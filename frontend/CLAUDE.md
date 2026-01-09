# Frontend Development Guidelines

## Project Overview

This directory contains the Next.js frontend application for the Todo Full-Stack Web Application. The frontend provides a responsive, user-friendly interface for managing todo tasks with secure authentication.

## Tech Stack
- **Framework:** Next.js 16+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Authentication:** Better Auth client
- **API Communication:** Built-in fetch with proper error handling

## Directory Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/             # Authentication-related pages
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── layout.tsx
│   ├── (app)/              # Application pages (protected)
│   │   ├── layout.tsx
│   │   ├── page.tsx        # Dashboard
│   │   ├── tasks/
│   │   │   ├── [id]/       # Task detail and edit
│   │   │   │   ├── page.tsx
│   │   │   │   └── edit/page.tsx
│   │   └── providers.tsx   # Global providers
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   ├── not-found.tsx       # 404 page
│   └── error.tsx           # Error boundary
├── components/             # Reusable UI components
│   ├── ui/                 # Base UI components
│   ├── auth/               # Authentication components
│   ├── tasks/              # Task-specific components
│   └── layout/             # Layout components
├── lib/                    # Utility functions and services
│   ├── auth/               # Authentication utilities
│   ├── api/                # API client and services
│   ├── types/              # TypeScript type definitions
│   └── utils/              # General utilities
├── styles/                 # Global styles
│   └── globals.css         # Tailwind and custom styles
├── hooks/                  # Custom React hooks
└── public/                 # Static assets
```

## Development Guidelines

### 1. Next.js App Router
- Use the App Router convention for all pages
- Implement proper loading states with `loading.tsx`
- Use error boundaries with `error.tsx`
- Implement not-found pages with `not-found.tsx`

### 2. TypeScript Usage
- Define all component props with TypeScript interfaces
- Use strict typing for API responses and form data
- Create shared type definitions in `lib/types/`
- Use utility types where appropriate

### 3. Styling with Tailwind CSS
- Use Tailwind utility classes for styling
- Create reusable component classes in `components/ui/`
- Use consistent color palette and spacing scale
- Implement responsive design with Tailwind's responsive prefixes

### 4. Authentication Integration
- Use Better Auth client for authentication flows
- Implement authentication wrapper for protected routes
- Handle token expiration gracefully
- Provide proper loading and error states

### 5. API Integration
- Create centralized API client in `lib/api/`
- Implement proper error handling and retry logic
- Use TypeScript interfaces for API responses
- Handle loading states with skeleton screens

## Component Development

### Naming Convention
- Use PascalCase for component names
- Group related components in feature-specific directories
- Use descriptive names that indicate component purpose

### Component Structure
- Create self-contained components with clear props interfaces
- Use composition over inheritance
- Implement proper accessibility attributes
- Include loading and error states where appropriate

### UI Component Guidelines
- Create base UI components in `components/ui/`
- Implement consistent design system
- Use Tailwind for styling with minimal custom CSS
- Ensure responsive design across all components

## State Management

### Client State
- Use React hooks for component-level state
- Use Context API for global application state
- Implement custom hooks for complex logic

### Server State
- Use React Query or SWR for server state management
- Implement proper caching and invalidation strategies
- Handle optimistic updates where appropriate

## Error Handling

### Client-Side Errors
- Implement global error boundary
- Show user-friendly error messages
- Provide clear recovery options
- Log errors appropriately

### API Errors
- Handle different HTTP status codes appropriately
- Show validation errors from API responses
- Implement retry mechanisms for network failures
- Provide offline state handling

## Performance Optimization

### Code Splitting
- Leverage Next.js automatic code splitting
- Use dynamic imports for non-critical components
- Implement route-based code splitting

### Image Optimization
- Use Next.js Image component for all images
- Implement proper image sizing and formats
- Use lazy loading for below-fold images

### Data Fetching
- Use Next.js data fetching methods appropriately
- Implement proper caching strategies
- Optimize API calls and reduce unnecessary requests

## Security Considerations

### Authentication
- Store JWT tokens securely (httpOnly cookies or secure storage)
- Implement proper token refresh mechanisms
- Handle token expiration gracefully

### Input Validation
- Validate all user inputs on the frontend
- Sanitize data before sending to backend
- Implement proper error handling for validation failures

### Content Security
- Use proper CSP headers
- Implement XSS protection
- Sanitize user-generated content

## Testing Guidelines

### Component Testing
- Write unit tests for individual components
- Use React Testing Library for component tests
- Test user interactions and state changes
- Implement snapshot testing for UI components

### Integration Testing
- Test API integration flows
- Test authentication workflows
- Test form submissions and validations

## Environment Configuration

### Environment Variables
```
NEXT_PUBLIC_API_URL=         # Backend API base URL
NEXT_PUBLIC_BETTER_AUTH_URL= # Better Auth base URL
```

### Required Variables
- `NEXT_PUBLIC_API_URL`: Base URL for backend API calls
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Base URL for authentication endpoints

## Deployment

### Build Process
- Use `npm run build` for production builds
- Optimize for performance with Next.js features
- Implement proper asset optimization

### Environment Setup
- Configure environment variables for different environments
- Set up proper API endpoints for each environment
- Implement proper error reporting for production

## Best Practices

### Code Organization
- Group related functionality in feature directories
- Keep components focused and reusable
- Use consistent naming conventions
- Maintain clear separation of concerns

### Performance
- Optimize component rendering
- Implement proper memoization
- Use efficient data structures
- Minimize bundle size

### Accessibility
- Follow WCAG guidelines
- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation support