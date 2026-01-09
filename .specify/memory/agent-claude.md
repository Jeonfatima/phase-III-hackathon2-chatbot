# Claude Agent Context - Phase II Foundation

## Project: Phase II – Todo Full-Stack Web Application

### Tech Stack
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: Better Auth (JWT)

### Current Phase: Foundation (Part 0) and Task CRUD API (Part 1)
- Monorepo structure with frontend/backend directories
- FastAPI backend bootstrap
- SQLModel setup with PostgreSQL connection
- Task model implementation
- Environment configuration
- **NEW**: Task CRUD API endpoints implementation with user isolation

### Database Schema
- Task model with fields: id (int, PK), user_id (UUID, FK), title (str), description (optional str), completed (bool), timestamps
- Indexes on user_id and completed fields
- Proper relationships and validation

### File Structure
```
backend/
├── main.py
├── requirements.txt
├── database/
│   ├── engine.py
│   ├── session.py
│   └── __init__.py
├── models/
│   ├── task.py
│   └── __init__.py
├── services/
│   ├── task_service.py
│   └── __init__.py
├── api/
│   ├── task_router.py
│   └── __init__.py
└── core/
    └── config.py

frontend/ (empty for now)

.env.example
.gitignore
```

### API Endpoints (Task CRUD)
- GET /api/{user_id}/tasks - Retrieve all tasks for a user
- POST /api/{user_id}/tasks - Create a new task for a user
- GET /api/{user_id}/tasks/{id} - Retrieve a specific task
- PUT /api/{user_id}/tasks/{id} - Update a specific task
- DELETE /api/{user_id}/tasks/{id} - Delete a specific task
- PATCH /api/{user_id}/tasks/{id}/complete - Update task completion status

### Environment Variables
- DATABASE_URL: PostgreSQL connection string
- Proper .env.example and .gitignore configuration

### Implementation Notes
- Use SQLModel for database models combining SQLAlchemy and Pydantic
- FastAPI for backend framework with automatic API documentation
- UUID for user_id field in Task model
- Automatic timestamp generation for created_at and updated_at
- Proper foreign key relationships between tasks and users
- **NEW**: User isolation by filtering all operations by user_id parameter in URL
- **NEW**: Consistent response models and proper validation
- **NEW**: Standard HTTP status codes (200, 201, 204, 404, 422) for error handling
- **NEW**: No JWT authentication in this phase (auth comes in Part 2)