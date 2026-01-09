import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from backend.main import app
from backend.models.task import TaskBase
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


def test_contract_post_task(client: TestClient, session: Session):
    """Contract test for POST /api/{user_id}/tasks"""
    # Create a test user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser"
    }
    # For now, we'll use a mock user_id since we're testing the contract
    user_id = 1

    # Test creating a task with valid data
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=task_data)

    # Assert the response status and structure
    assert response.status_code == 201

    response_data = response.json()
    assert "id" in response_data
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["completed"] == task_data["completed"]
    assert response_data["user_id"] == user_id


def test_contract_get_all_tasks(client: TestClient):
    """Contract test for GET /api/{user_id}/tasks"""
    user_id = 1

    # Test getting all tasks for a user
    response = client.get(f"/api/{user_id}/tasks")

    # Should return 200 with an empty list if no tasks exist
    assert response.status_code == 200
    assert response.json() == []


def test_contract_get_individual_task(client: TestClient, session: Session):
    """Contract test for GET /api/{user_id}/tasks/{id}"""
    user_id = 1

    # First create a task to retrieve
    task_data = {
        "title": "Contract Test Task",
        "description": "Task for contract testing",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Now retrieve the specific task
    response = client.get(f"/api/{user_id}/tasks/{task_id}")

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["completed"] == task_data["completed"]
    assert response_data["user_id"] == user_id


def test_contract_post_task_invalid_data(client: TestClient):
    """Contract test for POST /api/{user_id}/tasks with invalid data"""
    user_id = 1

    # Test with missing title (required field)
    invalid_task_data = {
        "description": "Test Description",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=invalid_task_data)

    # Should return 422 for validation error
    assert response.status_code == 422


def test_contract_post_task_empty_title(client: TestClient):
    """Contract test for POST /api/{user_id}/tasks with empty title"""
    user_id = 1

    # Test with empty title (should fail validation)
    invalid_task_data = {
        "title": "",
        "description": "Test Description",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=invalid_task_data)

    # Should return 422 for validation error
    assert response.status_code == 422


def test_contract_put_task(client: TestClient, session: Session):
    """Contract test for PUT /api/{user_id}/tasks/{id}"""
    user_id = 1

    # First create a task to update
    original_task_data = {
        "title": "Original Task Title",
        "description": "Original description",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Update the task
    updated_task_data = {
        "title": "Updated Task Title",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=updated_task_data)

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["title"] == updated_task_data["title"]
    assert response_data["description"] == updated_task_data["description"]
    assert response_data["completed"] == updated_task_data["completed"]
    assert response_data["user_id"] == user_id


def test_contract_put_task_invalid_data(client: TestClient, session: Session):
    """Contract test for PUT /api/{user_id}/tasks/{id} with invalid data"""
    user_id = 1

    # First create a task to update
    original_task_data = {
        "title": "Original Task Title",
        "description": "Original description",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Try to update with invalid data (empty title)
    invalid_task_data = {
        "title": "",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=invalid_task_data)

    # Should return 422 for validation error
    assert response.status_code == 422


def test_contract_delete_task(client: TestClient, session: Session):
    """Contract test for DELETE /api/{user_id}/tasks/{id}"""
    user_id = 1

    # First create a task to delete
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted in contract test",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Verify the task exists before deletion
    response = client.get(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 200

    # Delete the task
    response = client.delete(f"/api/{user_id}/tasks/{task_id}")

    # Assert the response
    assert response.status_code == 204

    # Verify the task no longer exists
    response = client.get(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 404


def test_contract_delete_task_not_found(client: TestClient):
    """Contract test for DELETE /api/{user_id}/tasks/{id} with non-existent task"""
    user_id = 1
    non_existent_task_id = 99999

    # Try to delete a non-existent task
    response = client.delete(f"/api/{user_id}/tasks/{non_existent_task_id}")

    # Should return 404
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_contract_patch_task_completion(client: TestClient, session: Session):
    """Contract test for PATCH /api/{user_id}/tasks/{id}/complete"""
    user_id = 1

    # First create a task to update completion status
    original_task_data = {
        "title": "Task for Completion Contract Test",
        "description": "This task will have its completion status updated in contract test",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Update the task completion status to True
    completion_data = {"completed": True}

    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json=completion_data)

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["completed"] == True
    assert response_data["title"] == original_task_data["title"]
    assert response_data["user_id"] == user_id

    # Update the task completion status back to False
    completion_data = {"completed": False}

    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json=completion_data)

    # Assert the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == task_id
    assert response_data["completed"] == False
    assert response_data["title"] == original_task_data["title"]
    assert response_data["user_id"] == user_id


def test_contract_patch_task_completion_invalid_data(client: TestClient, session: Session):
    """Contract test for PATCH /api/{user_id}/tasks/{id}/complete with invalid data"""
    user_id = 1

    # First create a task to update completion status
    original_task_data = {
        "title": "Task for Completion Contract Test",
        "description": "This task will have its completion status updated in contract test",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=original_task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Try to update with invalid completion value (non-boolean)
    invalid_completion_data = {"completed": "not_a_boolean"}

    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json=invalid_completion_data)

    # Should return 422 for validation error
    assert response.status_code == 422

    # Try to update with missing completion field
    missing_field_data = {"not_completed": True}

    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json=missing_field_data)

    # Should return 422 for validation error
    assert response.status_code == 422