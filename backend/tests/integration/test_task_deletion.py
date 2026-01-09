import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from backend.main import app
from backend.database.session import get_session
from backend.database.engine import engine
from backend.models.user import User


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


def test_integration_delete_task(client: TestClient, session: Session):
    """Integration test for deleting a task"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task to delete
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "completed": False
    }

    response = client.post(f"/api/{user.id}/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Verify the task exists before deletion
    response = client.get(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 200

    # Delete the task
    response = client.delete(f"/api/{user.id}/tasks/{task_id}")

    # Assert the response
    assert response.status_code == 204

    # Verify the task no longer exists
    response = client.get(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 404


def test_integration_delete_task_not_found(client: TestClient, session: Session):
    """Integration test for deleting a non-existent task"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Try to delete a task that doesn't exist
    non_existent_task_id = 99999

    response = client.delete(f"/api/{user.id}/tasks/{non_existent_task_id}")

    # Should return 404
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_integration_delete_task_user_isolation(client: TestClient, session: Session):
    """Integration test to verify user isolation in task deletion"""
    # Create two test users
    user1 = User(email="user1@example.com", username="user1")
    user2 = User(email="user2@example.com", username="user2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create a task for user1
    task_data = {
        "title": "User1 Task",
        "description": "This task belongs to user1",
        "completed": False
    }

    response = client.post(f"/api/{user1.id}/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Verify user1 can delete their task
    response = client.delete(f"/api/{user1.id}/tasks/{task_id}")
    assert response.status_code == 204

    # Create another task for user1
    response = client.post(f"/api/{user1.id}/tasks", json=task_data)
    assert response.status_code == 201
    created_task2 = response.json()
    task_id2 = created_task2["id"]

    # Verify user2 cannot delete user1's task
    response = client.delete(f"/api/{user2.id}/tasks/{task_id2}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

    # Clean up by deleting the task as user1
    response = client.delete(f"/api/{user1.id}/tasks/{task_id2}")
    assert response.status_code == 204


def test_integration_delete_task_invalid_user_id(client: TestClient):
    """Integration test for deleting a task with invalid user ID"""
    # Use an invalid user ID
    invalid_user_id = -1
    invalid_task_id = 1

    response = client.delete(f"/api/{invalid_user_id}/tasks/{invalid_task_id}")

    # Should return 400 for invalid user ID
    assert response.status_code == 400