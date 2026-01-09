from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import List
from database.session import get_session
from models.task import Task, TaskBase, TaskCreate, TaskUpdate
from services.task_service import TaskService
from auth import JWTBearer
from auth.middleware import get_current_user

router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: int,
    task_data: TaskCreate,
    request: Request,
    token_data: dict = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user
    """
    # Validate that user_id is a positive integer
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID must be a positive integer"
        )

    # Verify that the user_id in the URL matches the user_id in the token
    # Better Auth typically stores user ID in the 'userId' field or 'sub' field
    token_user_id_str = token_data.get("userId") or token_data.get("sub")
    if not token_user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )

    # Convert to int for comparison
    token_user_id = int(token_user_id_str)
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    # Create the task
    task = TaskService.create_task(session, user_id, task_data)
    return task


@router.get("/tasks", response_model=List[Task])
def get_all_tasks(
    user_id: int,
    request: Request,
    token_data: dict = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the specified user
    """
    # Validate that user_id is a positive integer
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID must be a positive integer"
        )

    # Verify that the user_id in the URL matches the user_id in the token
    # Better Auth typically stores user ID in the 'userId' field or 'sub' field
    token_user_id_str = token_data.get("userId") or token_data.get("sub")
    if not token_user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )

    # Convert to int for comparison
    token_user_id = int(token_user_id_str)
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    tasks = TaskService.get_all_tasks(session, user_id)
    return tasks


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    user_id: int,
    task_id: int,
    request: Request,
    token_data: dict = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the specified user
    """
    # Validate that IDs are positive integers
    if user_id <= 0 or task_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID and Task ID must be positive integers"
        )

    # Verify that the user_id in the URL matches the user_id in the token
    # Better Auth typically stores user ID in the 'userId' field or 'sub' field
    token_user_id_str = token_data.get("userId") or token_data.get("sub")
    if not token_user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )

    # Convert to int for comparison
    token_user_id = int(token_user_id_str)
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    task = TaskService.get_task_by_id(session, user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the specified user"
        )

    return task


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    request: Request,
    token_data: dict = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the specified user
    """
    # Validate that IDs are positive integer
    if user_id <= 0 or task_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID and Task ID must be positive integers"
        )

    # Verify that the user_id in the URL matches the user_id in the token
    # Better Auth typically stores user ID in the 'userId' field or 'sub' field
    token_user_id_str = token_data.get("userId") or token_data.get("sub")
    if not token_user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )

    # Convert to int for comparison
    token_user_id = int(token_user_id_str)
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    task = TaskService.get_task_by_id(session, user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the specified user"
        )

    updated_task = TaskService.update_task(session, user_id, task_id, task_data)
    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: int,
    task_id: int,
    request: Request,
    token_data: dict = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the specified user
    """
    # Validate that IDs are positive integers
    if user_id <= 0 or task_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID and Task ID must be positive integers"
        )

    # Verify that the user_id in the URL matches the user_id in the token
    # Better Auth typically stores user ID in the 'userId' field or 'sub' field
    token_user_id_str = token_data.get("userId") or token_data.get("sub")
    if not token_user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )

    # Convert to int for comparison
    token_user_id = int(token_user_id_str)
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    task = TaskService.get_task_by_id(session, user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the specified user"
        )

    success = TaskService.delete_task(session, user_id, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the specified user"
        )

    return


@router.patch("/tasks/{task_id}/complete", response_model=Task)
def update_task_completion(
    user_id: int,
    task_id: int,
    completion_data: dict,
    request: Request,
    token_data: dict = Depends(JWTBearer()),
    session: Session = Depends(get_session)
):
    """
    Update the completion status of a specific task by ID for the specified user
    """
    # Validate that IDs are positive integers
    if user_id <= 0 or task_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID and Task ID must be positive integers"
        )

    # Verify that the user_id in the URL matches the user_id in the token
    # Better Auth typically stores user ID in the 'userId' field or 'sub' field
    token_user_id_str = token_data.get("userId") or token_data.get("sub")
    if not token_user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID"
        )

    # Convert to int for comparison
    token_user_id = int(token_user_id_str)
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    # Validate that completion_data has the 'completed' field
    if "completed" not in completion_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Request must include 'completed' field with boolean value"
        )

    completed = completion_data["completed"]
    if not isinstance(completed, bool):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="'completed' field must be a boolean value"
        )

    task = TaskService.get_task_by_id(session, user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to the specified user"
        )

    updated_task = TaskService.update_task_completion(session, user_id, task_id, completed)
    return updated_task