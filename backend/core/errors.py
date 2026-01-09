from fastapi import HTTPException, status
from typing import Optional


class TaskException(HTTPException):
    """Base exception class for task-related errors"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class TaskNotFoundException(TaskException):
    """Raised when a task is not found"""
    def __init__(self, task_id: int, user_id: int):
        super().__init__(
            detail=f"Task with ID {task_id} not found for user {user_id}",
            status_code=status.HTTP_404_NOT_FOUND
        )


class UserNotFoundException(TaskException):
    """Raised when a user is not found"""
    def __init__(self, user_id: int):
        super().__init__(
            detail=f"User with ID {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationErrorException(TaskException):
    """Raised when validation fails"""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class UnauthorizedAccessException(TaskException):
    """Raised when a user tries to access resources they don't own"""
    def __init__(self):
        super().__init__(
            detail="You are not authorized to access this resource",
            status_code=status.HTTP_403_FORBIDDEN
        )