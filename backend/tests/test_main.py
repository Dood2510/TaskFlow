from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_create_and_get_task():
    # Create a task
    response = client.post("/tasks", json={
        "title": "Write pytest tests",
        "description": "Testing the API",
        "completed": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Write pytest tests"
    assert "id" in data

    task_id = data["id"]

    # Fetch it back
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Write pytest tests"


def test_get_nonexistent_task():
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_delete_task():
    # Create a task to delete
    create_response = client.post("/tasks", json={
        "title": "Temporary task",
        "completed": False
    })
    task_id = create_response.json()["id"]

    # Delete it
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    # Confirm it's gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404