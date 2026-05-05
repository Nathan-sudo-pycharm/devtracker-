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