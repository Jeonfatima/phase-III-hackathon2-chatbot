# Backend Development Guidelines

## Project Overview

This directory contains the FastAPI backend application for the Todo Full-Stack Web Application. The backend provides secure REST API endpoints for managing todo tasks with JWT-based authentication and PostgreSQL database integration.

## Tech Stack
- **Framework:** Python FastAPI
- **Database:** Neon Serverless PostgreSQL
- **ORM:** SQLModel
- **Authentication:** Better Auth with JWT
- **API Documentation:** Automatic OpenAPI/Swagger generation

## Directory Structure
```
backend/
├── main.py               # Application entry point
├── api/                  # API route definitions
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── tasks.py          # Task management endpoints
│   └── deps.py           # Dependency injection
├── models/               # SQLModel database models
│   ├── __init__.py
│   ├── user.py           # User model
│   ├── task.py           # Task model
│   └── base.py           # Base model configuration
├── schemas/              # Pydantic schemas for validation
│   ├── __init__.py
│   ├── user.py           # User schemas
│   ├── task.py           # Task schemas
│   └── auth.py           # Authentication schemas
├── database/             # Database connection and setup
│   ├── __init__.py
│   ├── session.py        # Database session management
│   └── engine.py         # Database engine configuration
├── auth/                 # Authentication logic
│   ├── __init__.py
│   ├── jwt.py            # JWT token handling
│   ├── security.py       # Security utilities
│   └── middleware.py     # Authentication middleware
├── core/                 # Core application configuration
│   ├── __init__.py
│   ├── config.py         # Application settings
│   └── security.py       # Security configuration
├── utils/                # Utility functions
│   ├── __init__.py
│   ├── validators.py     # Input validators
│   └── helpers.py        # Helper functions
└── tests/                # Test suite
    ├── __init__.py
    ├── test_auth.py      # Authentication tests
    ├── test_tasks.py     # Task API tests
    └── conftest.py       # Test configuration
```

## Development Guidelines

### 1. FastAPI Best Practices
- Use Pydantic models for request/response validation
- Implement proper HTTP status codes
- Leverage FastAPI's automatic API documentation
- Use dependency injection for shared functionality
- Implement async functions where appropriate

### 2. SQLModel Usage
- Define models using SQLModel with proper relationships
- Use proper foreign key constraints
- Implement proper indexing strategies
- Follow consistent naming conventions
- Use UUIDs for user IDs and auto-increment for task IDs

### 3. Authentication Implementation
- Use JWT tokens for stateless authentication
- Implement token verification middleware
- Enforce user ownership of resources
- Use BETTER_AUTH_SECRET for token signing
- Handle token expiration appropriately

### 4. Database Operations
- Use proper database sessions and transactions
- Implement connection pooling
- Follow SQL injection prevention practices
- Use parameterized queries
- Implement proper error handling for database operations

## API Development

### Endpoint Structure
- Follow RESTful conventions for endpoint design
- Use consistent URL patterns: `/api/{user_id}/tasks/{id}`
- Implement proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Return appropriate HTTP status codes
- Use consistent response format

### Request/Response Validation
- Define Pydantic schemas for all requests/responses
- Implement proper input validation
- Use type hints consistently
- Handle validation errors gracefully

### Error Handling
- Use FastAPI's exception handlers
- Return consistent error response format
- Log errors appropriately
- Don't expose internal error details to clients

## Security Implementation

### Authentication Flow
- Verify JWT tokens using BETTER_AUTH_SECRET
- Extract user_id from token claims
- Validate URL user_id matches token user_id
- Return 401 for invalid tokens, 403 for user mismatch

### Input Validation
- Validate all input parameters
- Use Pydantic models for automatic validation
- Implement custom validators when needed
- Sanitize inputs to prevent injection attacks

### Data Access Control
- Implement user ownership checks
- Prevent unauthorized data access
- Use proper database permissions
- Log security-relevant events

## Database Design

### Models
- Use SQLModel for database models
- Define proper relationships between models
- Implement proper indexing for performance
- Use UUIDs for user IDs and auto-increment for task IDs
- Include created_at and updated_at timestamps

### Schema Validation
- Define Pydantic schemas for API validation
- Use different schemas for input vs output
- Implement proper field constraints
- Use type hints consistently

### Migration Strategy
- Use Alembic for database migrations
- Maintain backward compatibility
- Include rollback scripts
- Test migrations in staging environment

## Performance Optimization

### Database Queries
- Use proper indexing strategies
- Implement query optimization
- Use connection pooling
- Minimize N+1 query problems
- Implement pagination for large datasets

### API Performance
- Use async functions where appropriate
- Implement proper caching strategies
- Optimize serialization/deserialization
- Use proper database session management

### Resource Management
- Properly close database connections
- Use context managers for resource cleanup
- Implement proper error handling
- Monitor resource usage

## Testing Guidelines

### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Test error conditions
- Maintain high test coverage

### Integration Tests
- Test API endpoints with real database
- Test authentication flows
- Test database operations
- Test error handling

### Test Data
- Use fixtures for test data setup
- Implement proper test database isolation
- Clean up test data after tests
- Use realistic test scenarios

## Environment Configuration

### Required Environment Variables
```
DATABASE_URL=              # PostgreSQL database connection string
BETTER_AUTH_SECRET=       # Secret for JWT token signing
BETTER_AUTH_URL=          # Base URL for authentication
JWT_EXPIRATION=           # Token expiration time (e.g., "24h")
DEBUG=                    # Debug mode (true/false)
```

### Configuration Management
- Use Pydantic Settings for configuration
- Implement environment-specific settings
- Validate required environment variables
- Use .env.example for documentation

## Deployment

### Production Setup
- Use uvicorn for production deployment
- Configure proper logging
- Set up monitoring and alerting
- Implement proper error reporting

### Security in Production
- Use HTTPS for all connections
- Configure proper CORS settings
- Implement rate limiting
- Secure environment variables
- Regular security updates

## API Documentation

### Automatic Documentation
- Leverage FastAPI's automatic OpenAPI generation
- Use proper docstrings for endpoints
- Include example requests/responses
- Maintain up-to-date documentation

### API Versioning
- Plan for API versioning strategy
- Use URL-based versioning if needed
- Maintain backward compatibility
- Document breaking changes

## Best Practices

### Code Organization
- Group related functionality in modules
- Use consistent naming conventions
- Follow Python style guides (PEP 8)
- Keep functions focused and small

### Error Handling
- Use proper exception hierarchy
- Log errors with appropriate context
- Return meaningful error messages
- Handle edge cases gracefully

### Performance
- Optimize database queries
- Use connection pooling
- Implement proper caching
- Monitor performance metrics

### Security
- Follow security best practices
- Regular security audits
- Keep dependencies updated
- Implement proper access controls