from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    """Helper — registers and logs in, returns token"""
    client.post("/auth/register", json={
        "email": "tasktest@test.com",
        "password": "testpass123"
    })
    response = client.post("/auth/login", data={
        "username": "tasktest@test.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]

def test_create_task():
    token = get_auth_token()
    # Pass token in Authorization header
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Testing",
        "status": "todo"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tasks_unauthorized():
    # No token — should fail
    response = client.get("/tasks/")
    assert response.status_code == 401