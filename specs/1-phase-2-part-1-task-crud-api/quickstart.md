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