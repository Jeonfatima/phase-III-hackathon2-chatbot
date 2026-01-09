# Database Schema Specification

## Database Overview

The application uses Neon Serverless PostgreSQL as the primary database, managed with SQLModel ORM. The schema ensures data integrity, proper relationships, and performance through appropriate indexing.

## Database Configuration

### Connection Settings
- **Database Provider:** Neon Serverless PostgreSQL
- **ORM:** SQLModel (combines SQLAlchemy and Pydantic)
- **Connection Pooling:** Managed by Neon's serverless architecture
- **Environment Variables:**
  - `DATABASE_URL`: Connection string for the PostgreSQL database

## Schema Design

### Users Table
The users table stores authentication information for registered users.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for email lookups (used for authentication)
CREATE INDEX idx_users_email ON users(email);

-- Index for creation date (used for user management)
CREATE INDEX idx_users_created_at ON users(created_at);
```

### Tasks Table
The tasks table stores todo items associated with specific users.

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Foreign key constraint linking to users table
    CONSTRAINT fk_tasks_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for user_id (critical for user-specific queries)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for completed status (used for filtering)
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Composite index for user_id and completed (used for user-specific filtering)
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Index for creation date (used for sorting and time-based queries)
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- Index for updated date (used for sync and recent changes)
CREATE INDEX idx_tasks_updated_at ON tasks(updated_at);
```

## SQLModel Definitions

### User Model
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    # tasks: List["Task"] = Relationship(back_populates="user")
```

### Task Model
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Data Integrity Constraints

### Primary Keys
- **users.id:** UUID, auto-generated, primary key
- **tasks.id:** SERIAL (auto-incrementing integer), primary key

### Foreign Keys
- **tasks.user_id:** References users.id with CASCADE delete

### Unique Constraints
- **users.email:** Unique constraint to prevent duplicate emails

### Not Null Constraints
- **users.email:** Required field
- **users.password_hash:** Required field
- **tasks.title:** Required field
- **tasks.completed:** Required field (defaults to false)

### Check Constraints
- **tasks.title:** Length between 1 and 255 characters
- **tasks.description:** Length up to 1000 characters (optional)

## Indexing Strategy

### Critical Indexes
1. **idx_tasks_user_id:** Essential for user-specific queries (single-user task retrieval)
2. **idx_tasks_completed:** Important for completion status filtering
3. **idx_tasks_user_completed:** Optimizes common user + status queries

### Performance Indexes
4. **idx_users_email:** Optimizes user authentication lookups
5. **idx_tasks_created_at:** Supports time-based sorting and filtering
6. **idx_tasks_updated_at:** Supports sync and recent changes queries

## Security Considerations

### Data Encryption
- **Password Hashing:** Passwords stored as bcrypt hashes (not plain text)
- **Connection Security:** All database connections use SSL/TLS encryption

### Access Control
- **Row-Level Security:** User isolation enforced by application logic (user_id matching)
- **No Direct Access:** Database access only through authenticated API endpoints

### Audit Trail
- **Timestamps:** All tables include created_at and updated_at fields
- **Automatic Updates:** Timestamps automatically managed by database triggers

## Migration Strategy

### Initial Schema
1. Create users table with basic structure
2. Create tasks table with foreign key relationship
3. Add indexes for performance
4. Set up foreign key constraints

### Future Migrations
- Use Alembic for schema evolution
- Maintain backward compatibility
- Include rollback scripts for all changes

## Performance Considerations

### Query Optimization
- Queries should utilize existing indexes
- Joins should be minimized in favor of separate queries
- Pagination implemented for large result sets

### Scaling Factors
- Neon Serverless automatically scales compute
- Proper indexing handles growing data volume
- Connection pooling managed by the platform

## Backup and Recovery

### Backup Strategy
- Neon's built-in backup system
- Point-in-time recovery capability
- Daily automated backups

### Recovery Procedures
- Database restoration from backups
- Data validation after recovery
- Application state verification

## Monitoring and Maintenance

### Monitoring
- Query performance metrics
- Connection pool utilization
- Storage usage tracking

### Maintenance
- Index optimization
- Statistics updates
- Vacuum and analyze operations (handled by Neon)