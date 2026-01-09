---
id: 1
title: phase-2-part-1-task-crud-api-spec
stage: spec
date: 2026-01-06
surface: agent
model: Claude Sonnet 4.5
feature: 1-phase-2-part-1-task-crud-api
branch: 1-phase-2-part-1-task-crud-api
user: claude-code
command: /sp.specify
labels: [spec, api, crud, task]
links:
  spec: specs/1-phase-2-part-1-task-crud-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-phase-2-part-1-task-crud-api/spec.md
 - specs/1-phase-2-part-1-task-crud-api/checklists/requirements.md
tests:
 - specs/1-phase-2-part-1-task-crud-api/spec.md
---

## Prompt

$ARGUMENTS

Title: Phase II – Part 1 (Backend Task CRUD API)

Scope:
Implement the REST API task CRUD endpoints using FastAPI + SQLModel.

Must follow:
- @specs/api/rest-endpoints.md
- @specs/features/task-crud.md
- @specs/database/schema.md

Requirements:
- Implement all task endpoints:
  GET    /api/{user_id}/tasks
  POST   /api/{user_id}/tasks
  GET    /api/{user_id}/tasks/{id}
  PUT    /api/{user_id}/tasks/{id}
  DELETE /api/{user_id}/tasks/{id}
  PATCH  /api/{user_id}/tasks/{id}/complete

Important:
- Accept {user_id} in URL and filter tasks by that user_id.
- For this part, do NOT enforce JWT yet (auth comes in Part 2).
- Add validation and consistent response models.
- Add basic error handling (404 for missing task, etc.)

Update specs only if needed for clarity. Do NOT implement code in this step.

## Response snapshot

# Feature Specification: Task CRUD API

**Feature Branch**: `1-phase-2-part-1-task-crud-api`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Phase II – Part 1 (Backend Task CRUD API)

Scope:
Implement the REST API task CRUD endpoints using FastAPI + SQLModel.

Must follow:
- @specs/api/rest-endpoints.md
- @specs/features/task-crud.md
- @specs/database/schema.md

Requirements:
- Implement all task endpoints:
  GET    /api/{user_id}/tasks
  POST   /api/{user_id}/tasks
  GET    /api/{user_id}/tasks/{id}
  PUT    /api/{user_id}/tasks/{id}
  DELETE /api/{user_id}/tasks/{id}
  PATCH  /api/{user_id}/tasks/{id}/complete

Important:
- Accept {user_id} in URL and filter tasks by that user_id.
- For this part, do NOT enforce JWT yet (auth comes in Part 2).
- Add validation and consistent response models.
- Add basic error handling (404 for missing task, etc.)

Update specs only if needed for clarity. Do NOT implement code in this step."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Tasks (Priority: P1)

A user needs to create new tasks associated with their account. The system must accept task data and store it in the database, associating it with the specified user ID.

**Why this priority**: This is the foundational capability that enables all other task operations. Without creating tasks, no other functionality is valuable.

**Independent Test**: Can be fully tested by sending a POST request to `/api/{user_id}/tasks` with task data and verifying the task is created and returned with appropriate status codes.

**Acceptance Scenarios**:

1. **Given** a valid user ID and task data, **When** user sends POST request to `/api/{user_id}/tasks`, **Then** system creates the task and returns it with 201 status
2. **Given** invalid task data, **When** user sends POST request to `/api/{user_id}/tasks`, **Then** system returns 422 validation error with details

---

### User Story 2 - Retrieve All User Tasks (Priority: P1)

A user needs to view all their tasks. The system must return all tasks associated with the specified user ID.

**Why this priority**: Essential for users to see their tasks and understand their current workload.

**Independent Test**: Can be fully tested by sending a GET request to `/api/{user_id}/tasks` and verifying the correct tasks are returned.

**Acceptance Scenarios**:

1. **Given** a valid user ID with existing tasks, **When** user sends GET request to `/api/{user_id}/tasks`, **Then** system returns all tasks for that user with 200 status
2. **Given** a valid user ID with no tasks, **When** user sends GET request to `/api/{user_id}/tasks`, **Then** system returns empty list with 200 status

---

### User Story 3 - Retrieve Individual Task (Priority: P2)

A user needs to view details of a specific task. The system must return the requested task if it belongs to the specified user.

**Why this priority**: Enables detailed task viewing and is prerequisite for other operations like updating or deleting specific tasks.

**Independent Test**: Can be fully tested by sending a GET request to `/api/{user_id}/tasks/{id}` and verifying the correct task is returned.

**Acceptance Scenarios**:

1. **Given** a valid user ID and existing task ID that belongs to that user, **When** user sends GET request to `/api/{user_id}/tasks/{id}`, **Then** system returns the task with 200 status
2. **Given** a valid user ID and task ID that does not belong to that user, **When** user sends GET request to `/api/{user_id}/tasks/{id}`, **Then** system returns 404 error
3. **Given** a valid user ID and non-existent task ID, **When** user sends GET request to `/api/{user_id}/tasks/{id}`, **Then** system returns 404 error

---

### User Story 4 - Update Task (Priority: P2)

A user needs to modify an existing task. The system must update the specified task if it belongs to the user.

**Why this priority**: Allows users to keep their tasks up-to-date with changing requirements or status.

**Independent Test**: Can be fully tested by sending a PUT request to `/api/{user_id}/tasks/{id}` with updated data and verifying the task is updated.

**Acceptance Scenarios**:

1. **Given** a valid user ID, existing task ID that belongs to that user, and updated task data, **When** user sends PUT request to `/api/{user_id}/tasks/{id}`, **Then** system updates the task and returns it with 200 status
2. **Given** a valid user ID and non-existent task ID, **When** user sends PUT request to `/api/{user_id}/tasks/{id}`, **Then** system returns 404 error
3. **Given** invalid task data, **When** user sends PUT request to `/api/{user_id}/tasks/{id}`, **Then** system returns 422 validation error

---

### User Story 5 - Delete Task (Priority: P2)

A user needs to remove a task. The system must delete the specified task if it belongs to the user.

**Why this priority**: Essential for task lifecycle management and keeping user task lists clean.

**Independent Test**: Can be fully tested by sending a DELETE request to `/api/{user_id}/tasks/{id}` and verifying the task is deleted.

**Acceptance Scenarios**:

1. **Given** a valid user ID and existing task ID that belongs to that user, **When** user sends DELETE request to `/api/{user_id}/tasks/{id}`, **Then** system deletes the task and returns 204 status
2. **Given** a valid user ID and non-existent task ID, **When** user sends DELETE request to `/api/{user_id}/tasks/{id}`, **Then** system returns 404 error

---

### User Story 6 - Mark Task as Complete (Priority: P3)

A user needs to mark a task as complete/incomplete. The system must update the completion status of the specified task if it belongs to the user.

**Why this priority**: Provides a streamlined way to update task status without requiring full task updates.

**Independent Test**: Can be fully tested by sending a PATCH request to `/api/{user_id}/tasks/{id}/complete` and verifying the completion status is updated.

**Acceptance Scenarios**:

1. **Given** a valid user ID and existing task ID that belongs to that user, **When** user sends PATCH request to `/api/{user_id}/tasks/{id}/complete` with completion status, **Then** system updates the task completion status and returns it with 200 status
2. **Given** a valid user ID and non-existent task ID, **When** user sends PATCH request to `/api/{user_id}/tasks/{id}/complete`, **Then** system returns 404 error

---

### Edge Cases

- What happens when a user tries to access another user's tasks?
- How does system handle invalid user IDs or task IDs?
- How does system handle malformed request data?
- What validation is applied to task fields (title, description, etc.)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide REST API endpoints for task CRUD operations using FastAPI and SQLModel
- **FR-002**: System MUST implement GET endpoint at `/api/{user_id}/tasks` to retrieve all tasks for a specific user
- **FR-003**: System MUST implement POST endpoint at `/api/{user_id}/tasks` to create a new task for a specific user
- **FR-004**: System MUST implement GET endpoint at `/api/{user_id}/tasks/{id}` to retrieve a specific task for a specific user
- **FR-005**: System MUST implement PUT endpoint at `/api/{user_id}/tasks/{id}` to update a specific task for a specific user
- **FR-006**: System MUST implement DELETE endpoint at `/api/{user_id}/tasks/{id}` to delete a specific task for a specific user
- **FR-007**: System MUST implement PATCH endpoint at `/api/{user_id}/tasks/{id}/complete` to update the completion status of a specific task for a specific user
- **FR-008**: System MUST filter all operations by the user_id parameter in the URL to ensure users can only access their own tasks
- **FR-009**: System MUST include proper validation for all input data and return appropriate error responses
- **FR-010**: System MUST use consistent response models for all endpoints
- **FR-011**: System MUST return 404 error when a requested task does not exist or does not belong to the specified user
- **FR-012**: System MUST return 422 error when request data fails validation
- **FR-013**: System MUST NOT enforce JWT authentication at this phase (auth comes in Part 2)

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with properties like title, description, completion status, timestamps, and associated user ID
- **User**: Represents a user account identified by user_id, with tasks associated to them

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 6 required REST endpoints are implemented and accessible according to the specification
- **SC-002**: Users can perform all CRUD operations on their own tasks with 95% success rate in testing
- **SC-003**: System properly filters tasks by user_id ensuring users cannot access other users' tasks
- **SC-004**: API returns appropriate error codes (404, 422) for invalid requests with 100% accuracy
- **SC-005**: All endpoints respond within 500ms under normal load conditions
- **SC-006**: Validation is applied consistently across all endpoints with appropriate error messages

## Outcome

- ✅ Impact: Created comprehensive specification for Phase II Part 1 task CRUD API with 6 REST endpoints
- 🧪 Tests: Specification includes acceptance scenarios for all user stories
- 📁 Files: Created spec.md and requirements checklist in specs/1-phase-2-part-1-task-crud-api/
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification captures all required endpoints and includes proper validation, error handling, and user isolation requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A