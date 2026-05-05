import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base

# Create all tables before tests run
# This runs migrations automatically for the test database
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c