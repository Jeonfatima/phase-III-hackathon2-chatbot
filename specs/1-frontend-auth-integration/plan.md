# Implementation Plan: Frontend UI + Better Auth Integration

**Feature**: 1-frontend-auth-integration
**Created**: 2026-01-07
**Status**: Draft

## Technical Context

This plan outlines the implementation of a Next.js frontend with Better Auth integration for the Todo application. The frontend will connect to an existing FastAPI backend that provides JWT-protected task management endpoints.

### Known Elements
- Backend API endpoints exist at `/api/{user_id}/tasks/*` with JWT authentication
- Better Auth integration required for authentication
- Frontend must be built in the existing `frontend/` directory
- UI must be sleek, modern, and hackathon-level polished
- Must follow existing specs for UI pages, components, task CRUD, authentication, and REST endpoints

### Unknown Elements
- [NEEDS CLARIFICATION] What is the exact structure of the Better Auth integration (configuration, provider setup)?
- [NEEDS CLARIFICATION] What are the exact API response formats from the backend?
- [NEEDS CLARIFICATION] What is the specific user ID format used in the backend (string vs number)?

## Constitution Check

This implementation aligns with the project constitution:
- ✅ Spec-Driven Development: Following the specified requirements from the feature spec
- ✅ Progressive Evolution Architecture: Building Phase II (Full-Stack Web) upon Phase I
- ✅ Domain Integrity: Maintaining consistent task attributes (id, title, description, completed)
- ✅ Clean Code and Minimalism: Implementing only required functionality
- ✅ Phase-Gated Implementation: Focusing on frontend implementation without backend changes
- ✅ Tool Chain Consistency: Using Claude Code and following established patterns

## Phase 0: Research

### Research Findings

#### Better Auth Integration
Better Auth provides a client-side SDK that can be integrated with Next.js applications. The integration typically involves:
- Installing the `better-auth` package
- Setting up a client instance with the auth endpoint
- Using hooks like `useAuth()` to manage authentication state
- The client automatically handles JWT token storage and retrieval

#### API Response Formats
Based on the backend code analysis:
- GET `/api/{user_id}/tasks` returns an array of task objects
- Task objects have: id (number), user_id (number), title (string), description (string), completed (boolean), created_at, updated_at
- POST `/api/{user_id}/tasks` returns a single task object on success (201)
- Other endpoints return task objects or 204 for DELETE

#### User ID Format
From the backend code, user_id is treated as an integer in the API endpoints and validation logic.

## Phase 1: Design

### Data Model
Based on the backend models, the frontend will work with these data structures:

**Task Interface:**
```typescript
interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}
```

**User Interface:**
```typescript
interface User {
  id: number;
  email: string;
  // Additional fields from Better Auth
}
```

### API Contract
The frontend will implement the following API calls:

1. **Authentication:**
   - `POST /api/auth/register` - User registration
   - `POST /api/auth/login` - User login
   - `POST /api/auth/logout` - User logout

2. **Task Management:**
   - `GET /api/{user_id}/tasks` - Get all tasks for user
   - `POST /api/{user_id}/tasks` - Create new task
   - `GET /api/{user_id}/tasks/{id}` - Get specific task
   - `PUT /api/{user_id}/tasks/{id}` - Update task
   - `DELETE /api/{user_id}/tasks/{id}` - Delete task
   - `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Frontend Architecture

#### Project Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── layout.tsx
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (app)/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── tasks/
│   │       ├── [id]/
│   │       │   ├── page.tsx
│   │       │   └── edit/
│   │       │       └── page.tsx
│   │       └── layout.tsx
│   ├── globals.css
│   └── layout.tsx
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── auth/
│   │   ├── login-form.tsx
│   │   ├── register-form.tsx
│   │   └── auth-layout.tsx
│   ├── tasks/
│   │   ├── task-card.tsx
│   │   ├── task-list.tsx
│   │   ├── task-form.tsx
│   │   └── empty-state.tsx
│   └── layout/
│       ├── header.tsx
│       └── sidebar.tsx
├── lib/
│   ├── api.ts
│   ├── auth.ts
│   └── types.ts
├── hooks/
│   ├── use-auth.ts
│   └── use-tasks.ts
├── providers/
│   └── auth-provider.tsx
└── package.json
```

#### API Client Implementation
A centralized API client in `/lib/api.ts` will:
- Automatically attach JWT tokens from Better Auth
- Handle 401/403 responses by redirecting to login
- Provide consistent error handling
- Include loading states

#### Authentication Flow
1. User visits `/login` or `/register`
2. Better Auth handles authentication
3. JWT token is stored and automatically attached to API requests
4. Protected routes check for valid authentication
5. Unauthenticated users are redirected to auth pages

## Phase 2: Implementation Steps

### Step 1: Project Setup
1. Initialize Next.js project in frontend directory (if not already done)
2. Install required dependencies: `next`, `react`, `react-dom`, `better-auth`, `tailwindcss`
3. Configure Tailwind CSS
4. Set up TypeScript configuration

### Step 2: Authentication Implementation
1. Set up Better Auth client configuration
2. Create authentication pages (login, register)
3. Implement auth provider and context
4. Create authentication components (forms, layouts)

### Step 3: API Client Development
1. Create `/lib/api.ts` with centralized API client
2. Implement JWT token handling
3. Add error handling for 401/403 responses
4. Create hooks for authentication state

### Step 4: UI Components Development
1. Create reusable UI components based on the component spec
2. Implement form components (InputField, Button, etc.)
3. Create task-specific components (TaskCard, TaskList, etc.)
4. Develop layout components (Header, Sidebar, etc.)

### Step 5: Protected Routes Implementation
1. Create app layout with authentication wrapper
2. Implement route protection
3. Add redirects for unauthenticated users
4. Create dashboard page to display tasks

### Step 6: Task Management Features
1. Implement task listing with filtering
2. Create task creation form
3. Implement task editing functionality
4. Add task deletion with confirmation
5. Create task completion toggle

### Step 7: UI Polish and Responsiveness
1. Apply Tailwind CSS styling consistently
2. Implement responsive design for mobile/desktop
3. Add loading states and error handling
4. Create empty states for task lists
5. Polish UI with modern design elements

### Step 8: Testing and Integration
1. Test authentication flow end-to-end
2. Verify all API calls work with backend
3. Test error handling scenarios
4. Validate responsive design
5. Perform final QA and polish

## Risk Assessment

### High-Risk Areas
1. **Authentication Integration**: Ensuring Better Auth properly integrates with JWT handling
2. **Backend Compatibility**: Verifying API endpoints match expected formats
3. **User ID Consistency**: Ensuring proper handling of user ID format across frontend/backend

### Mitigation Strategies
1. Start with basic auth integration and test early
2. Create API mock layer initially, then integrate with real backend
3. Implement comprehensive error handling for API responses

## Success Criteria Verification

The implementation will meet the success criteria from the spec:
- ✅ Users can complete signup/signin in under 30 seconds
- ✅ 95% of authenticated users can perform CRUD operations on tasks
- ✅ UI works on mobile (320px) and desktop (1200px+) screen sizes
- ✅ 99% of API requests include proper JWT authentication headers
- ✅ Users receive feedback during loading/error states
- ✅ Unauthenticated users redirected to auth page within 1 second
- ✅ All UI components use Tailwind CSS consistently
- ✅ Application supports modern browsers