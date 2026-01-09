# UI Pages Specification

## Page Structure Overview

The application follows Next.js App Router conventions with a clear page structure that supports authentication flows and task management functionality.

## Page Routes

### Public Routes (No Authentication Required)

#### /
- **Path:** `/`
- **Title:** "Todo App - Welcome"
- **Description:** Landing page for unauthenticated users with app overview and call-to-action to sign up
- **Components:**
  - Hero section with app description
  - Feature highlights
  - Sign up/login call-to-action buttons
  - Footer with navigation links
- **Layout:** Root layout without authentication wrapper
- **SEO:** Welcome page with app description for search engines

#### /auth/login
- **Path:** `/auth/login`
- **Title:** "Login - Todo App"
- **Description:** User authentication page with email and password fields
- **Components:**
  - Login form with email and password inputs
  - "Forgot password" link (future enhancement)
  - "Don't have an account?" signup link
  - Form validation and error handling
- **Layout:** Auth layout without navigation
- **Behavior:** Redirects to dashboard on successful login
- **SEO:** Login page with security focus

#### /auth/register
- **Path:** `/auth/register`
- **Title:** "Register - Todo App"
- **Description:** User registration page with email and password fields
- **Components:**
  - Registration form with email and password inputs
  - Password strength indicator
  - "Already have an account?" login link
  - Form validation and error handling
- **Layout:** Auth layout without navigation
- **Behavior:** Redirects to dashboard on successful registration
- **SEO:** Registration page with account creation focus

### Protected Routes (Authentication Required)

#### /
- **Path:** `/`
- **Title:** "My Tasks - Todo App"
- **Description:** Main dashboard showing user's todo tasks with CRUD operations
- **Components:**
  - Navigation header with user profile and logout
  - Task creation form (title, description)
  - Task list with filtering options
  - Individual task cards with title, description, completion toggle, edit/delete buttons
  - Empty state when no tasks exist
  - Pagination for large task lists (future enhancement)
- **Layout:** App layout with authentication wrapper
- **Behavior:**
  - Shows loading state while fetching tasks
  - Real-time updates after CRUD operations
  - Filtering by completion status
- **SEO:** Dashboard page with user's tasks (noindex for privacy)

#### /tasks/[id]
- **Path:** `/tasks/[id]`
- **Title:** "Task Details - Todo App"
- **Description:** Detailed view of a specific task with full information and editing capabilities
- **Components:**
  - Task detail header with title and completion status
  - Task description section
  - Creation and update timestamps
  - Edit and delete action buttons
  - Back to dashboard link
- **Layout:** App layout with authentication wrapper
- **Behavior:**
  - Shows loading state while fetching task
  - 404 page if task doesn't exist or doesn't belong to user
  - Navigation to edit page when editing
- **SEO:** Task detail page (noindex for privacy)

#### /tasks/[id]/edit
- **Path:** `/tasks/[id]/edit`
- **Title:** "Edit Task - Todo App"
- **Description:** Form to edit an existing task's details
- **Components:**
  - Task editing form with title and description fields
  - Completion status toggle
  - Save and cancel buttons
  - Form validation and error handling
- **Layout:** App layout with authentication wrapper
- **Behavior:**
  - Pre-fills form with existing task data
  - Redirects back to task detail on save
  - Redirects back to dashboard on cancel
- **SEO:** Edit task page (noindex for privacy)

### Special Pages

#### /404
- **Path:** `/404`
- **Title:** "Page Not Found - Todo App"
- **Description:** Custom 404 error page for non-existent routes
- **Components:**
  - Error message with 404 status
  - Descriptive text about the missing page
  - Link back to dashboard or home
- **Layout:** Minimal layout without complex components
- **Behavior:** Displays when no route matches

#### /500
- **Path:** `/500`
- **Title:** "Server Error - Todo App"
- **Description:** Custom 500 error page for server-side errors
- **Components:**
  - Error message with 500 status
  - Descriptive text about the server error
  - Link back to dashboard or home
  - Option to report the error (future enhancement)
- **Layout:** Minimal layout without complex components
- **Behavior:** Displays when server error occurs

## Layout Structure

### Root Layout (app/layout.tsx)
- **Purpose:** Base layout for all pages
- **Components:**
  - HTML document structure
  - Global styles and fonts
  - Meta tags and SEO elements
  - Global providers (theme, auth context, etc.)

### Auth Layout (app/(auth)/layout.tsx)
- **Purpose:** Layout for authentication pages
- **Components:**
  - Minimal header or branding
  - Main content container with centered forms
  - Footer with legal links
- **Behavior:** No navigation sidebar or user-specific content

### App Layout (app/(app)/layout.tsx)
- **Purpose:** Layout for authenticated application pages
- **Components:**
  - Navigation sidebar with app links
  - Top navigation bar with user profile
  - Main content area
  - Global notifications/toasts
- **Behavior:** Includes authentication wrapper that redirects unauthenticated users

## Authentication Wrapper

### Behavior:
- Checks for valid authentication token on protected routes
- Redirects to login page if no valid token exists
- Displays loading state while checking authentication status
- Provides user context to child components

## SEO and Metadata

### Common Meta Tags:
- **Title:** Dynamic titles based on page content
- **Description:** Page-specific descriptions
- **Viewport:** Responsive viewport settings
- **Charset:** UTF-8 encoding
- **Author:** Application author information

### Page-Specific Considerations:
- **Public pages:** Include in search engine indexes
- **Protected pages:** Use robots noindex for privacy
- **Auth pages:** Clear purpose and security-focused descriptions

## Responsive Design

### Breakpoints:
- **Mobile:** 0px - 640px
- **Tablet:** 641px - 1024px
- **Desktop:** 1025px+

### Responsive Behaviors:
- **Navigation:** Collapsible sidebar on mobile
- **Forms:** Full-width on mobile, compact on desktop
- **Task lists:** Grid layout on desktop, single column on mobile
- **Buttons:** Larger touch targets on mobile devices

## Accessibility

### ARIA Labels:
- Form inputs with proper labels
- Navigation landmarks
- Status updates for screen readers
- Focus management for keyboard navigation

### Keyboard Navigation:
- Tab order follows logical sequence
- Focus indicators for interactive elements
- Keyboard shortcuts for common actions (future enhancement)

## Performance Considerations

### Loading States:
- Skeleton screens during data fetching
- Optimistic updates for immediate feedback
- Error boundaries for graceful error handling

### Caching:
- Client-side caching of user data
- Prefetching for navigation optimization
- Image optimization and lazy loading (if applicable)

## Error Handling

### Client-Specific Errors:
- Network request failures
- Authentication token expiration
- Form validation errors
- User permission errors

### Display Strategy:
- Inline error messages for form validation
- Toast notifications for API errors
- Dedicated error pages for major issues
- Graceful degradation for unavailable features