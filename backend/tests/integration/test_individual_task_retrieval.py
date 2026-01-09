import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from backend.main import app
from backend.database.session import get_session
from backend.database.engine import engine
from backend.models.user import User
from backend.models.task import Task


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


def test_integration_get_individual_task(client: TestClient, session: Session):
    """Integration test for getting a specific task by ID for a user"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a task for the user
    task_data = {
        "title": "Individual Task Test",
        "description": "This is a test for retrieving individual tasks",
        "completed": False
    }

    response = client.post(f"/api/{user.id}/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Now get the specific task
    response = client.get(f"/api/{user.id}/tasks/{task_id}")

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["completed"] == task_data["completed"]
    assert response_data["user_id"] == user.id


def test_integration_get_individual_task_not_found(client: TestClient, session: Session):
    """Integration test for getting a non-existent task"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Try to get a task that doesn't exist
    non_existent_task_id = 99999
    response = client.get(f"/api/{user.id}/tasks/{non_existent_task_id}")

    # Should return 404
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_integration_get_individual_task_user_isolation(client: TestClient, session: Session):
    """Integration test to verify user isolation in individual task retrieval"""
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

    # Verify user1 can access their task
    response = client.get(f"/api/{user1.id}/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

    # Verify user2 cannot access user1's task
    response = client.get(f"/api/{user2.id}/tasks/{task_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_integration_get_individual_task_invalid_user_id(client: TestClient):
    """Integration test for getting a task with invalid user ID"""
    # Use an invalid user ID
    invalid_user_id = -1
    invalid_task_id = 1

    response = client.get(f"/api/{invalid_user_id}/tasks/{invalid_task_id}")

    # Should return 400 for invalid user ID
    assert response.status_code == 400