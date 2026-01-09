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


def test_integration_get_all_tasks(client: TestClient, session: Session):
    """Integration test for getting all tasks for a user"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # First, create some tasks for the user
    task_data_1 = {
        "title": "Integration Test Task 1",
        "description": "This is the first test task",
        "completed": False
    }

    task_data_2 = {
        "title": "Integration Test Task 2",
        "description": "This is the second test task",
        "completed": True
    }

    # Create the tasks
    response1 = client.post(f"/api/{user.id}/tasks", json=task_data_1)
    assert response1.status_code == 201

    response2 = client.post(f"/api/{user.id}/tasks", json=task_data_2)
    assert response2.status_code == 201

    # Now get all tasks for the user
    response = client.get(f"/api/{user.id}/tasks")

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2

    # Check that both tasks are present
    titles = [task["title"] for task in response_data]
    assert task_data_1["title"] in titles
    assert task_data_2["title"] in titles

    # Verify that the task details are correct
    for task in response_data:
        assert "id" in task
        assert "user_id" in task
        assert task["user_id"] == user.id


def test_integration_get_all_tasks_empty(client: TestClient, session: Session):
    """Integration test for getting all tasks when user has no tasks"""
    # Create a test user
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Get all tasks for the user (should be empty)
    response = client.get(f"/api/{user.id}/tasks")

    # Should return 200 with an empty list
    assert response.status_code == 200
    assert response.json() == []


def test_integration_get_all_tasks_user_isolation(client: TestClient, session: Session):
    """Integration test to verify user isolation in task retrieval"""
    # Create two test users
    user1 = User(email="user1@example.com", username="user1")
    user2 = User(email="user2@example.com", username="user2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    # Create tasks for user1
    task_data_1 = {
        "title": "User1 Task 1",
        "description": "Task for user1",
        "completed": False
    }

    response = client.post(f"/api/{user1.id}/tasks", json=task_data_1)
    assert response.status_code == 201

    # Create tasks for user2
    task_data_2 = {
        "title": "User2 Task 1",
        "description": "Task for user2",
        "completed": True
    }

    response = client.post(f"/api/{user2.id}/tasks", json=task_data_2)
    assert response.status_code == 201

    # Get tasks for user1 - should only see their own task
    response = client.get(f"/api/{user1.id}/tasks")
    assert response.status_code == 200
    user1_tasks = response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["title"] == task_data_1["title"]

    # Get tasks for user2 - should only see their own task
    response = client.get(f"/api/{user2.id}/tasks")
    assert response.status_code == 200
    user2_tasks = response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["title"] == task_data_2["title"]