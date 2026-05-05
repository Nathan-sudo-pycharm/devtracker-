from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import os

# Secret key to sign JWT tokens — keep this private in .env
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

# Algorithm used to sign the token
ALGORITHM = "HS256"

# Token expires after 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# bcrypt is the industry standard for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tells FastAPI where to look for the token (Authorization header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    """Convert plain text password to hashed version"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Check if plain password matches the hashed one"""
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    """Create a JWT token with expiry"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Decode JWT token and return the current logged-in user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Find user in database
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user