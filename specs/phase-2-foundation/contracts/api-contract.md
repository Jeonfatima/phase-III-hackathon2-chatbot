# API Contract: Phase II – Part 0 (Foundation)

## Database Connection Contract

### Environment Variables
- **DATABASE_URL**: PostgreSQL connection string
  - Format: `postgresql://username:password@host:port/database`
  - Required: Yes
  - Example: `postgresql://user:pass@localhost:5432/todoapp`

## Task Model Contract

### Task Object Structure
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Sample task",
  "description": "Task description (optional)",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Field Definitions
- **id**: Integer, auto-incrementing primary key
- **user_id**: UUID string, references user who owns the task
- **title**: String, 1-255 characters, required
- **description**: String, optional, variable length
- **completed**: Boolean, default false
- **created_at**: ISO 8601 datetime string with timezone
- **updated_at**: ISO 8601 datetime string with timezone

### Validation Rules
- Title must be 1-255 characters
- user_id must be valid UUID format
- completed must be boolean value
- created_at and updated_at are server-generated

## Future API Endpoints (Foundation for later implementation)

### GET /api/{user_id}/tasks
- Purpose: Retrieve all tasks for a specific user
- Requires: Valid authentication token
- Authorization: Token user must match URL user_id

### POST /api/{user_id}/tasks
- Purpose: Create a new task for a user
- Requires: Valid authentication token and task data
- Authorization: Token user must match URL user_id

### GET /api/{user_id}/tasks/{id}
- Purpose: Retrieve a specific task
- Requires: Valid authentication token
- Authorization: Token user must match URL user_id

### PUT /api/{user_id}/tasks/{id}
- Purpose: Update a specific task
- Requires: Valid authentication token and task data
- Authorization: Token user must match URL user_id

### DELETE /api/{user_id}/tasks/{id}
- Purpose: Delete a specific task
- Requires: Valid authentication token
- Authorization: Token user must match URL user_id

### PATCH /api/{user_id}/tasks/{id}/complete
- Purpose: Toggle task completion status
- Requires: Valid authentication token and completion status
- Authorization: Token user must match URL user_id