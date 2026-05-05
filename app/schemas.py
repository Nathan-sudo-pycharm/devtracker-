from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- Task Schemas ---

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- User Schemas ---

class UserCreate(BaseModel):
    # EmailStr validates it's a real email format
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Token Schema ---

class Token(BaseModel):
    # This is what gets returned after login
    access_token: str
    token_type: str  # always "bearer"