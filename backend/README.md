# Todo API Backend

This is the backend service for the Todo Full-Stack Web Application, built with FastAPI and SQLModel.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
```
Then edit `.env` to set your `DATABASE_URL`.

3. Start the development server:
```bash
cd backend
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (required)
- `DEBUG`: Enable debug mode (optional, default: false)

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /db-health` - Database health check

## Configuration

The application uses a configuration system that loads settings from environment variables. See `.env.example` for required variables.