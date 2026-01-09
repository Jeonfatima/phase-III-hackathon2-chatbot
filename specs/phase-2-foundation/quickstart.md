# Quickstart: Phase II – Part 0 (Foundation)

## Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL database (or Neon Serverless account)

### 1. Clone and Navigate to Backend
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` to set your `DATABASE_URL`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
```

### 5. Start the Application
```bash
uvicorn main:app --reload
```

## Directory Structure
```
backend/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── database/            # Database connection setup
│   ├── engine.py        # Database engine
│   ├── session.py       # Session management
│   └── __init__.py
├── models/              # Data models
│   ├── task.py          # Task model
│   └── __init__.py
└── core/                # Core configuration
    └── config.py
```

## Key Components

### Database Setup
- Uses SQLModel with PostgreSQL
- Connection via DATABASE_URL environment variable
- Automatic connection pooling

### Task Model
- Implements the specification from data-model.md
- Includes validation and proper relationships
- Ready for CRUD operations

## Next Steps
1. Implement API endpoints for task operations
2. Add authentication layer
3. Create frontend application