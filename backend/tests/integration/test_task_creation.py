import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
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


def test_integration_task_creation(client: TestClient, session: Session):
    """Integration test for task creation"""
    # Create a test user first
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Test creating a task
    task_data = {
        "title": "Integration Test Task",
        "description": "This is a test task for integration testing",
        "completed": False
    }

    response = client.post(f"/api/{user.id}/tasks", json=task_data)

    # Assert the response
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["completed"] == task_data["completed"]
    assert response_data["user_id"] == user.id
    assert "id" in response_data
    assert "created_at" in response_data
    assert "updated_at" in response_data

    # Verify the task was actually created in the database
    created_task = session.get(Task, response_data["id"])
    assert created_task is not None
    assert created_task.title == task_data["title"]
    assert created_task.user_id == user.id


def test_integration_task_creation_user_isolation(client: TestClient, session: Session):
    """Integration test to verify user isolation in task creation"""
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
        "description": "Task for user1",
        "completed": False
    }

    response = client.post(f"/api/{user1.id}/tasks", json=task_data)
    assert response.status_code == 201

    response_data = response.json()
    task_id = response_data["id"]

    # Verify that user1 can access their task
    response = client.get(f"/api/{user1.id}/tasks/{task_id}")
    assert response.status_code == 200

    # Verify that user2 cannot access user1's task
    response = client.get(f"/api/{user2.id}/tasks/{task_id}")
    assert response.status_code == 404