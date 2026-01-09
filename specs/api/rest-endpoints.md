# REST API Endpoints Specification

## API Overview

The REST API provides endpoints for managing todo tasks with proper authentication and user isolation. All endpoints require JWT authentication and enforce user ownership of resources.

## Base URL

```
https://api.yourdomain.com/api
```

## Authentication

All endpoints (except authentication endpoints) require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

The token must be verified by the backend, and the user_id in the token must match the user_id in the URL path for user-specific endpoints.

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* optional error details */ }
  }
}
```

## Endpoints

### Authentication Endpoints

#### POST /auth/register
- **Description:** Register a new user account
- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```
- **Success Response:** 201 Created with JWT token
- **Error Responses:** 400 (validation), 409 (email exists)

#### POST /auth/login
- **Description:** Authenticate user and return JWT token
- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```
- **Success Response:** 200 OK with JWT token
- **Error Responses:** 400 (validation), 401 (invalid credentials)

#### POST /auth/logout
- **Description:** Logout user and invalidate session
- **Headers:** Authorization: Bearer <token>
- **Success Response:** 200 OK
- **Error Responses:** 401 (invalid token)

### Task Management Endpoints

#### GET /{user_id}/tasks
- **Description:** Get all tasks for a specific user
- **Headers:** Authorization: Bearer <token>
- **Path Parameters:**
  - `user_id`: User ID from token must match this value
- **Query Parameters:**
  - `completed` (optional): Filter by completion status (true/false)
  - `limit` (optional): Number of tasks to return (default: 50)
  - `offset` (optional): Number of tasks to skip (default: 0)
- **Success Response:** 200 OK with array of task objects
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": "user123",
      "title": "Sample task",
      "description": "Task description",
      "completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```
- **Error Responses:** 401 (unauthorized), 403 (user mismatch), 404 (user not found)

#### POST /{user_id}/tasks
- **Description:** Create a new task for a specific user
- **Headers:** Authorization: Bearer <token>
- **Path Parameters:**
  - `user_id`: User ID from token must match this value
- **Request Body:**
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "completed": false
}
```
- **Success Response:** 201 Created with created task object
- **Error Responses:** 400 (validation), 401 (unauthorized), 403 (user mismatch)

#### GET /{user_id}/tasks/{id}
- **Description:** Get a specific task by ID
- **Headers:** Authorization: Bearer <token>
- **Path Parameters:**
  - `user_id`: User ID from token must match this value
  - `id`: Task ID
- **Success Response:** 200 OK with task object
- **Error Responses:** 401 (unauthorized), 403 (user mismatch), 404 (task not found)

#### PUT /{user_id}/tasks/{id}
- **Description:** Update a specific task completely
- **Headers:** Authorization: Bearer <token>
- **Path Parameters:**
  - `user_id`: User ID from token must match this value
  - `id`: Task ID
- **Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```
- **Success Response:** 200 OK with updated task object
- **Error Responses:** 400 (validation), 401 (unauthorized), 403 (user mismatch), 404 (task not found)

#### DELETE /{user_id}/tasks/{id}
- **Description:** Delete a specific task
- **Headers:** Authorization: Bearer <token>
- **Path Parameters:**
  - `user_id`: User ID from token must match this value
  - `id`: Task ID
- **Success Response:** 204 No Content
- **Error Responses:** 401 (unauthorized), 403 (user mismatch), 404 (task not found)

#### PATCH /{user_id}/tasks/{id}/complete
- **Description:** Toggle or set completion status of a task
- **Headers:** Authorization: Bearer <token>
- **Path Parameters:**
  - `user_id`: User ID from token must match this value
  - `id`: Task ID
- **Request Body:**
```json
{
  "completed": true
}
```
- **Success Response:** 200 OK with updated task object
- **Error Responses:** 400 (validation), 401 (unauthorized), 403 (user mismatch), 404 (task not found)

## Request Validation

### Common Validation Rules:
- **User ID:** Must match the authenticated user's ID from token
- **Task ID:** Must be a valid integer
- **Title:** Required, 1-255 characters
- **Description:** Optional, max 1000 characters
- **Completed:** Boolean value (true/false)

### Validation Error Format:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "field": "error_message"
    }
  }
}
```

## HTTP Status Codes

### Success Codes:
- **200 OK:** Request successful
- **201 Created:** Resource created successfully
- **204 No Content:** Request successful, no content to return

### Client Error Codes:
- **400 Bad Request:** Invalid request format or validation error
- **401 Unauthorized:** Missing or invalid authentication token
- **403 Forbidden:** Valid token but user doesn't own resource
- **404 Not Found:** Requested resource doesn't exist
- **409 Conflict:** Request conflicts with current state (e.g., duplicate email)
- **422 Unprocessable Entity:** Semantic errors in request content

### Server Error Codes:
- **500 Internal Server Error:** Unexpected server error
- **503 Service Unavailable:** Service temporarily unavailable

## Rate Limiting

- **Authentication endpoints:** Limited to 10 requests per minute per IP
- **API endpoints:** Limited to 1000 requests per hour per user

## Security Headers

All API responses should include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- Proper CORS headers for frontend integration

## API Versioning

API versioning will be handled through URL paths (e.g., `/api/v1/{user_id}/tasks`). For Phase II, all endpoints use the default version (no version specified in path).