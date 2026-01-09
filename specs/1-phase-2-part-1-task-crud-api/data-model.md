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