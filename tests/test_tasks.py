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

def test_create_task_missing_title():
    """Task without title should fail"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks/", json={
        "description": "No title here"
    }, headers=headers)
    # FastAPI validates required fields automatically → 422
    assert response.status_code == 422

def test_get_task_not_found():
    """Getting a task that doesn't exist should return 404"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks/99999", headers=headers)
    assert response.status_code == 404

def test_update_task():
    """Update a task and verify the change"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    # First create a task
    create = client.post("/tasks/", json={
        "title": "Old Title",
        "status": "todo"
    }, headers=headers)
    task_id = create.json()["id"]
    # Then update it
    response = client.put(f"/tasks/{task_id}", json={
        "title": "New Title",
        "status": "in_progress"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["status"] == "in_progress"

def test_delete_task():
    """Delete a task and verify it's gone"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Create a task
    create = client.post("/tasks/", json={
        "title": "To be deleted",
        "status": "todo"
    }, headers=headers)
    task_id = create.json()["id"]
    # Delete it
    delete = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete.status_code == 200
    # Verify it's gone
    get = client.get(f"/tasks/{task_id}", headers=headers)
    assert get.status_code == 404