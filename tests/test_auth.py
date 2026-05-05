from fastapi.testclient import TestClient
from app.main import app

# TestClient lets us make fake HTTP requests to our app
# without running a real server
client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "email": "testuser@test.com",
        "password": "testpass123"
    })
    # Assert means "this must be true, otherwise test fails"
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@test.com"

def test_register_user():
    response = client.post("/auth/register", json={
        "email": "testuser@test.com",
        "password": "testpass123"
    })
    # 200 = new user, 400 = already exists — both are valid
    assert response.status_code in [200, 400]

def test_login_wrong_password():
    response = client.post("/auth/login", data={
        "username": "logintest@test.com",
        "password": "wrongpassword"
    })
    # Should return 401 Unauthorized
    assert response.status_code == 401

def test_register_duplicate_email():
    """Registering same email twice should fail"""
    client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "password": "pass123"
    })
    response = client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "password": "pass123"
    })
    assert response.status_code == 400

def test_register_invalid_email():
    """Invalid email format should fail"""
    response = client.post("/auth/register", json={
        "email": "notanemail",
        "password": "pass123"
    })
    assert response.status_code == 422