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


def test_integration_update_task_completion(client: TestClient, session: Session):
    """Integration test for updating task completion status"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task to update completion status
    original_task_data = {
        "title": "Task for Completion Test",
        "description": "This task will have its completion status updated",
        "completed": False
    }

    response = client.post(f"/api/{user.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Update the task completion status to True
    completion_data = {"completed": True}

    response = client.patch(f"/api/{user.id}/tasks/{task_id}/complete", json=completion_data)

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["completed"] == True
    assert response_data["title"] == original_task_data["title"]
    assert response_data["user_id"] == user.id

    # Verify the task was actually updated in the database
    response = client.get(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["completed"] == True


def test_integration_update_task_completion_to_false(client: TestClient, session: Session):
    """Integration test for updating task completion status from True to False"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a completed task
    original_task_data = {
        "title": "Completed Task",
        "description": "This task is already completed",
        "completed": True
    }

    response = client.post(f"/api/{user.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Update the task completion status to False
    completion_data = {"completed": False}

    response = client.patch(f"/api/{user.id}/tasks/{task_id}/complete", json=completion_data)

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["completed"] == False
    assert response_data["title"] == original_task_data["title"]
    assert response_data["user_id"] == user.id

    # Verify the task was actually updated in the database
    response = client.get(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["completed"] == False


def test_integration_update_task_completion_not_found(client: TestClient, session: Session):
    """Integration test for updating completion status of a non-existent task"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Try to update completion status of a task that doesn't exist
    non_existent_task_id = 99999
    completion_data = {"completed": True}

    response = client.patch(f"/api/{user.id}/tasks/{non_existent_task_id}/complete", json=completion_data)

    # Should return 404
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_integration_update_task_completion_user_isolation(client: TestClient, session: Session):
    """Integration test to verify user isolation in task completion updates"""
    # Create two test users
    user1 = User(email="user1@example.com", username="user1")
    user2 = User(email="user2@example.com", username="user2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create a task for user1
    original_task_data = {
        "title": "User1 Task",
        "description": "Task for user1",
        "completed": False
    }

    response = client.post(f"/api/{user1.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Verify user1 can update their task completion status
    completion_data = {"completed": True}
    response = client.patch(f"/api/{user1.id}/tasks/{task_id}/complete", json=completion_data)
    assert response.status_code == 200
    assert response.json()["completed"] == True

    # Create another task for user1
    response = client.post(f"/api/{user1.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task2 = response.json()
    task_id2 = created_task2["id"]

    # Verify user2 cannot update user1's task completion status
    completion_data = {"completed": True}
    response = client.patch(f"/api/{user2.id}/tasks/{task_id2}/complete", json=completion_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_integration_update_task_completion_invalid_data(client: TestClient, session: Session):
    """Integration test for updating task completion with invalid data"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task to update completion status
    original_task_data = {
        "title": "Task for Completion Test",
        "description": "This task will have its completion status updated",
        "completed": False
    }

    response = client.post(f"/api/{user.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Try to update with invalid data (non-boolean completion status)
    invalid_completion_data = {"completed": "not_a_boolean"}

    response = client.patch(f"/api/{user.id}/tasks/{task_id}/complete", json=invalid_completion_data)

    # Should return 422 for validation error
    assert response.status_code == 422

    # Try to update with missing completion field
    missing_field_data = {"not_completed": True}

    response = client.patch(f"/api/{user.id}/tasks/{task_id}/complete", json=missing_field_data)

    # Should return 422 for validation error
    assert response.status_code == 422