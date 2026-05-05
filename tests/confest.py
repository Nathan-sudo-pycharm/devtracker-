import pytest
from fastapi.testclient import TestClient
from app.main import app

# TestClient simulates real HTTP requests without running a server
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c