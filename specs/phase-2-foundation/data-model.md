# Data Model: Phase II – Part 0 (Foundation)

## Task Entity

### Fields
- **id**: Integer (Primary Key, Auto-increment)
  - Purpose: Unique identifier for each task
  - Constraints: Required, Unique, Auto-generated
- **user_id**: UUID (Foreign Key)
  - Purpose: Links task to user who owns it
  - Constraints: Required, References users table
- **title**: String (Max 255 characters)
  - Purpose: Task title/description
  - Constraints: Required, Max 255 characters
- **description**: Text (Optional)
  - Purpose: Detailed task description
  - Constraints: Optional, Variable length
- **completed**: Boolean
  - Purpose: Completion status of the task
  - Constraints: Required, Default: false
- **created_at**: DateTime (with timezone)
  - Purpose: Timestamp when task was created
  - Constraints: Required, Auto-generated
- **updated_at**: DateTime (with timezone)
  - Purpose: Timestamp when task was last updated
  - Constraints: Required, Auto-generated

### Relationships
- **user_id** → **users.id**: Many-to-One relationship
  - A task belongs to one user
  - A user can have many tasks

### Validation Rules
- Title must not be empty
- Title must be less than 255 characters
- Completed field must be boolean
- user_id must reference a valid user

### Indexes
- Index on `user_id` for efficient user-specific queries
- Index on `completed` for filtering by completion status
- Composite index on `user_id` and `completed` for combined filtering

## Implementation Notes

### SQLModel Definition
The Task model will be implemented using SQLModel with the following structure:
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    title: str = Field(max_length=255)
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### State Transitions
- Task is created with `completed: false` by default
- Task can transition from `completed: false` to `completed: true`
- Task can transition from `completed: true` to `completed: false`
- Task can be deleted (permanent removal)