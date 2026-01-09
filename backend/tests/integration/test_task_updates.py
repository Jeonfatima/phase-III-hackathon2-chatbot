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


def test_integration_update_task(client: TestClient, session: Session):
    """Integration test for updating a task"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task to update
    original_task_data = {
        "title": "Original Task Title",
        "description": "Original description",
        "completed": False
    }

    response = client.post(f"/api/{user.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Update the task
    updated_task_data = {
        "title": "Updated Task Title",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(f"/api/{user.id}/tasks/{task_id}", json=updated_task_data)

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["title"] == updated_task_data["title"]
    assert response_data["description"] == updated_task_data["description"]
    assert response_data["completed"] == updated_task_data["completed"]
    assert response_data["user_id"] == user.id

    # Verify the task was actually updated in the database
    response = client.get(f"/api/{user.id}/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["title"] == updated_task_data["title"]
    assert retrieved_task["description"] == updated_task_data["description"]
    assert retrieved_task["completed"] == updated_task_data["completed"]


def test_integration_update_task_partial_fields(client: TestClient, session: Session):
    """Integration test for updating only some fields of a task"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task to update
    original_task_data = {
        "title": "Original Task Title",
        "description": "Original description",
        "completed": False
    }

    response = client.post(f"/api/{user.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Update only the title and completion status (not the description)
    updated_task_data = {
        "title": "Updated Task Title",
        "completed": True
    }

    response = client.put(f"/api/{user.id}/tasks/{task_id}", json=updated_task_data)

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["title"] == updated_task_data["title"]
    assert response_data["description"] == original_task_data["description"]  # Should remain unchanged
    assert response_data["completed"] == updated_task_data["completed"]
    assert response_data["user_id"] == user.id


def test_integration_update_task_not_found(client: TestClient, session: Session):
    """Integration test for updating a non-existent task"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Try to update a task that doesn't exist
    non_existent_task_id = 99999
    updated_task_data = {
        "title": "Updated Task Title",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(f"/api/{user.id}/tasks/{non_existent_task_id}", json=updated_task_data)

    # Should return 404
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_integration_update_task_user_isolation(client: TestClient, session: Session):
    """Integration test to verify user isolation in task updates"""
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

    # Verify user1 can update their task
    updated_task_data = {
        "title": "Updated User1 Task",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(f"/api/{user1.id}/tasks/{task_id}", json=updated_task_data)
    assert response.status_code == 200

    # Create another task for user1
    response = client.post(f"/api/{user1.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task2 = response.json()
    task_id2 = created_task2["id"]

    # Verify user2 cannot update user1's task
    response = client.put(f"/api/{user2.id}/tasks/{task_id2}", json=updated_task_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_integration_update_task_invalid_data(client: TestClient, session: Session):
    """Integration test for updating a task with invalid data"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task to update
    original_task_data = {
        "title": "Original Task Title",
        "description": "Original description",
        "completed": False
    }

    response = client.post(f"/api/{user.id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Try to update with invalid data (empty title)
    invalid_task_data = {
        "title": "",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(f"/api/{user.id}/tasks/{task_id}", json=invalid_task_data)

    # Should return 422 for validation error
    assert response.status_code == 422