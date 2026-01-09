---
id: 2
title: phase-2-part-1-task-crud-api-plan
stage: plan
date: 2026-01-06
surface: agent
model: Claude Sonnet 4.5
feature: 1-phase-2-part-1-task-crud-api
branch: 1-phase-2-part-1-task-crud-api
user: claude-code
command: /sp.plan
labels: [plan, api, crud, task, fastapi, sqlmodel]
links:
  spec: specs/1-phase-2-part-1-task-crud-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-phase-2-part-1-task-crud-api/plan.md
 - specs/1-phase-2-part-1-task-crud-api/research.md
 - specs/1-phase-2-part-1-task-crud-api/data-model.md
 - specs/1-phase-2-part-1-task-crud-api/quickstart.md
 - specs/1-phase-2-part-1-task-crud-api/contracts/task-api-openapi.yaml
 - .specify/memory/agent-claude.md
tests:
 - specs/1-phase-2-part-1-task-crud-api/plan.md
 - specs/1-phase-2-part-1-task-crud-api/research.md
 - specs/1-phase-2-part-1-task-crud-api/data-model.md
 - specs/1-phase-2-part-1-task-crud-api/quickstart.md
---

## Prompt

$ARGUMENTS

## Response snapshot

# Implementation Plan: Task CRUD API

**Branch**: `1-phase-2-part-1-task-crud-api` | **Date**: 2026-01-06 | **Spec**: [specs/1-phase-2-part-1-task-crud-api/spec.md](specs/1-phase-2-part-1-task-crud-api/spec.md)
**Input**: Feature specification from `/specs/1-phase-2-part-1-task-crud-api/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of REST API task CRUD endpoints using FastAPI and SQLModel. The system will provide 6 endpoints for task management operations (GET, POST, PUT, DELETE, PATCH) with user isolation based on user_id parameter. All operations will be secured by filtering tasks based on the user_id in the URL to ensure users can only access their own tasks. The API will include proper validation, consistent response models, and appropriate error handling.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, uvicorn
**Storage**: SQL database (SQLite for development, PostgreSQL for production - to be defined in database schema)
**Testing**: pytest with FastAPI test client
**Target Platform**: Linux server (web API)
**Project Type**: Web API backend
**Performance Goals**: All endpoints respond within 500ms under normal load conditions
**Constraints**: <200ms p95 response time for API calls, proper user isolation to prevent cross-user data access
**Scale/Scope**: Support multiple concurrent users accessing their own tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the constitution:
1. Spec-Driven Development: ✅ Following the spec created in the previous step
2. Progressive Evolution Architecture: ✅ This is Phase II Part 1, building upon previous phases
3. Domain Integrity: ✅ Maintaining consistent task attributes (id, title, description, completed status)
4. Clean Code and Minimalism: ✅ Following clean code principles with minimal dependencies
5. Phase-Gated Implementation: ✅ Following Phase II requirements
6. Tool Chain Consistency: ✅ Using Claude Code and Spec-Kit Plus as required

## Project Structure

### Documentation (this feature)

```text
specs/1-phase-2-part-1-task-crud-api/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── task_router.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   └── main.py
└── tests/
    ├── unit/
    │   └── test_task_service.py
    ├── integration/
    │   └── test_task_api.py
    └── contract/
        └── test_task_contracts.py
```

**Structure Decision**: Web application structure selected with backend API containing models, services, API routes, and database modules. This follows standard FastAPI project organization with separation of concerns between data models, business logic, and API endpoints.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

# Research: Task CRUD API Implementation

## Decision: FastAPI and SQLModel Framework Choice
**Rationale**: FastAPI provides automatic API documentation (Swagger/OpenAPI), built-in validation with Pydantic, and high performance. SQLModel combines SQLAlchemy's power with Pydantic's validation, making it ideal for FastAPI applications. This combination aligns with the specification requirements and provides type safety, validation, and automatic API documentation.

**Alternatives considered**:
- Flask + SQLAlchemy: More manual work required for validation and documentation
- Django REST Framework: Heavier framework than needed for this API-focused task
- Express.js: Would require changing from Python ecosystem

## Decision: User Isolation Strategy
**Rationale**: Filtering by user_id in the URL path parameter ensures users can only access their own tasks. This approach is straightforward to implement and understand. Each request will validate that the requested task belongs to the specified user_id, returning 404 if it doesn't.

**Alternatives considered**:
- JWT token-based user identification: Will be implemented in Part 2 as specified
- Session-based authentication: Not needed for this API-first approach
- Database-level row security: More complex than necessary for this implementation

## Decision: Error Handling Approach
**Rationale**: Using standard HTTP status codes (200, 201, 204, 404, 422) provides clear communication about request outcomes. FastAPI's built-in exception handling with custom HTTPException will be used for consistent error responses.

**Alternatives considered**:
- Custom error codes: Would make the API less standard
- Generic error responses: Would provide less specific feedback to API consumers

## Decision: Validation Implementation
**Rationale**: Pydantic models will be used for request/response validation, leveraging FastAPI's automatic validation. This ensures data integrity and provides clear error messages to API consumers.

**Alternatives considered**:
- Manual validation: More error-prone and verbose
- Third-party validation libraries: Unnecessary when Pydantic is already part of the stack

## Decision: API Endpoint Design
**Rationale**: Following REST conventions with the specified endpoints ensures consistency and predictability. The design matches the requirements in the specification exactly.

**Alternatives considered**:
- GraphQL: Would require different approach than specified
- RPC-style endpoints: Less RESTful and predictable

# Data Model: Task CRUD API

## Task Entity

**Entity Name**: Task

**Fields**:
- `id` (Integer, Primary Key, Auto-increment): Unique identifier for the task
- `title` (String, Required): Title of the task (max 255 characters)
- `description` (String, Optional): Detailed description of the task (max 1000 characters)
- `completed` (Boolean, Default: False): Completion status of the task
- `user_id` (Integer, Required, Foreign Key): ID of the user who owns this task
- `created_at` (DateTime, Auto-generated): Timestamp when the task was created
- `updated_at` (DateTime, Auto-generated): Timestamp when the task was last updated

**Validation Rules**:
- `title` must be 1-255 characters long
- `description` can be null or 1-1000 characters long
- `completed` defaults to False when creating new tasks
- `user_id` must reference an existing user
- `created_at` and `updated_at` are automatically set by the system

**Relationships**:
- Many-to-One: Task belongs to User (via user_id foreign key)

## User Entity

**Entity Name**: User

**Fields**:
- `id` (Integer, Primary Key, Auto-increment): Unique identifier for the user
- `email` (String, Required, Unique): User's email address
- `username` (String, Required, Unique): User's chosen username
- `created_at` (DateTime, Auto-generated): Timestamp when the user was created
- `updated_at` (DateTime, Auto-generated): Timestamp when the user was last updated

**Validation Rules**:
- `email` must be a valid email format and unique
- `username` must be 3-50 characters long and unique
- `created_at` and `updated_at` are automatically set by the system

**Relationships**:
- One-to-Many: User has many Tasks

## State Transitions

**Task Completion State**:
- Default state: `completed = False`
- When task is marked complete: `completed = True`
- When task is marked incomplete: `completed = False`

## Database Constraints

- Unique constraint on Task (id, user_id) to prevent ID conflicts across users
- Foreign key constraint ensuring user_id references valid User
- Index on user_id for efficient filtering by user
- Index on (user_id, completed) for efficient queries by user and completion status

# Quickstart: Task CRUD API

## Prerequisites

- Python 3.13+
- pip package manager
- Virtual environment tool (venv, conda, etc.)

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install fastapi sqlmodel uvicorn pytest httpx
```

### 3. Project Structure

Create the following directory structure:

```
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── task_router.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py
│   └── main.py
└── tests/
    ├── unit/
    │   └── test_task_service.py
    ├── integration/
    │   └── test_task_api.py
    └── contract/
        └── test_task_contracts.py
```

### 4. Initialize Database

```python
# In your main application startup
from src.database.database import create_db_and_tables

create_db_and_tables()
```

### 5. Run the Application

```bash
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Create a Task
```
POST /api/{user_id}/tasks
Content-Type: application/json

{
  "title": "My Task",
  "description": "Task description (optional)",
  "completed": false
}
```

### Get All Tasks for User
```
GET /api/{user_id}/tasks
```

### Get a Specific Task
```
GET /api/{user_id}/tasks/{task_id}
```

### Update a Task
```
PUT /api/{user_id}/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true
}
```

### Delete a Task
```
DELETE /api/{user_id}/tasks/{task_id}
```

### Update Task Completion Status
```
PATCH /api/{user_id}/tasks/{task_id}/complete
Content-Type: application/json

{
  "completed": true
}
```

## Testing

Run the tests:

```bash
pytest
```

## Environment Variables

Create a `.env` file in the backend directory:

```
DATABASE_URL=sqlite:///./test.db
```

# OpenAPI Contract for Task API

```yaml
openapi: 3.0.3
info:
  title: Task Management API
  description: API for managing user tasks with CRUD operations
  version: 1.0.0
servers:
  - url: http://localhost:8000
    description: Development server
paths:
  /api/{user_id}/tasks:
    get:
      summary: Get all tasks for a user
      parameters:
        - name: user_id
          in: path
          required: true
          description: ID of the user
          schema:
            type: integer
      responses:
        '200':
          description: List of tasks for the user
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Task'
        '404':
          description: User not found
    post:
      summary: Create a new task for a user
      parameters:
        - name: user_id
          in: path
          required: true
          description: ID of the user
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          description: User not found
        '422':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ValidationError'
  /api/{user_id}/tasks/{id}:
    get:
      summary: Get a specific task
      parameters:
        - name: user_id
          in: path
          required: true
          description: ID of the user
          schema:
            type: integer
        - name: id
          in: path
          required: true
          description: ID of the task
          schema:
            type: integer
      responses:
        '200':
          description: Task details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          description: Task not found or does not belong to user
    put:
      summary: Update a specific task
      parameters:
        - name: user_id
          in: path
          required: true
          description: ID of the user
          schema:
            type: integer
        - name: id
          in: path
          required: true
          description: ID of the task
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Task updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          description: Task not found or does not belong to user
        '422':
          description: Validation error
    delete:
      summary: Delete a specific task
      parameters:
        - name: user_id
          in: path
          required: true
          description: ID of the user
          schema:
            type: integer
        - name: id
          in: path
          required: true
          description: ID of the task
          schema:
            type: integer
      responses:
        '204':
          description: Task deleted successfully
        '404':
          description: Task not found or does not belong to user
  /api/{user_id}/tasks/{id}/complete:
    patch:
      summary: Update task completion status
      parameters:
        - name: user_id
          in: path
          required: true
          description: ID of the user
          schema:
            type: integer
        - name: id
          in: path
          required: true
          description: ID of the task
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                completed:
                  type: boolean
                  description: New completion status for the task
              required:
                - completed
      responses:
        '200':
          description: Task completion status updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          description: Task not found or does not belong to user
        '422':
          description: Validation error
components:
  schemas:
    Task:
      type: object
      properties:
        id:
          type: integer
          description: Unique identifier for the task
          example: 1
        title:
          type: string
          description: Title of the task
          example: "Buy groceries"
        description:
          type: string
          description: Detailed description of the task
          example: "Milk, bread, eggs"
        completed:
          type: boolean
          description: Completion status of the task
          example: false
        user_id:
          type: integer
          description: ID of the user who owns this task
          example: 1
        created_at:
          type: string
          format: date-time
          description: Timestamp when the task was created
          example: "2023-01-01T12:00:00Z"
        updated_at:
          type: string
          format: date-time
          description: Timestamp when the task was last updated
          example: "2023-01-01T12:00:00Z"
      required:
        - id
        - title
        - completed
        - user_id
        - created_at
        - updated_at
    TaskCreate:
      type: object
      properties:
        title:
          type: string
          description: Title of the task (1-255 characters)
          example: "Buy groceries"
          minLength: 1
          maxLength: 255
        description:
          type: string
          description: Detailed description of the task (optional)
          example: "Milk, bread, eggs"
          maxLength: 1000
        completed:
          type: boolean
          description: Initial completion status of the task
          example: false
      required:
        - title
    TaskUpdate:
      type: object
      properties:
        title:
          type: string
          description: Title of the task (1-255 characters)
          example: "Buy groceries"
          minLength: 1
          maxLength: 255
        description:
          type: string
          description: Detailed description of the task (optional)
          example: "Milk, bread, eggs"
          maxLength: 1000
        completed:
          type: boolean
          description: New completion status of the task
          example: true
      required:
        - title
    ValidationError:
      type: object
      properties:
        detail:
          type: array
          items:
            type: object
            properties:
              loc:
                type: array
                items:
                  type: string
                description: Location of the validation error
              msg:
                type: string
                description: Error message
              type:
                type: string
                description: Type of validation error
```

## Outcome

- ✅ Impact: Created comprehensive implementation plan for Phase II Part 1 task CRUD API with all required artifacts
- 🧪 Tests: Defined contract tests in the OpenAPI specification
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/task-api-openapi.yaml, and updated agent context
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan covers all required endpoints with proper user isolation, validation, and error handling as specified

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A