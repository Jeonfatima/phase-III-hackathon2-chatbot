# System Architecture

## Architecture Overview

The Phase II Todo Full-Stack Web Application follows a client-server architecture with a clear separation of concerns between frontend and backend components. The system uses a monorepo structure with distinct frontend and backend directories.

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │   Backend        │    │   Database       │
│   (Next.js)     │◄──►│   (FastAPI)      │◄──►│   (PostgreSQL)   │
│                 │    │                  │    │                  │
│ • Next.js App   │    │ • REST API       │    │ • Neon Serverless│
│ • TypeScript    │    │ • Authentication │    │ • SQLModel ORM   │
│ • Tailwind CSS  │    │ • JWT Auth       │    │ • User isolation │
└─────────────────┘    └──────────────────┘    └──────────────────┘
```

### Component Architecture

#### Frontend Architecture (Next.js 16+ App Router)
- **Directory Structure:** App Router convention with nested routing
- **State Management:** Client-side state for UI interactions
- **Authentication:** JWT token management in browser storage
- **API Communication:** HTTP requests to backend REST API
- **Styling:** Tailwind CSS for responsive, component-based styling
- **Type Safety:** TypeScript interfaces for API contracts

#### Backend Architecture (FastAPI)
- **Framework:** FastAPI with async support
- **API Layer:** RESTful endpoints with proper HTTP status codes
- **Authentication:** Better Auth integration for JWT handling
- **Business Logic:** Service layer for task operations
- **Data Access:** SQLModel ORM for database operations
- **Security:** Input validation, authentication middleware, user authorization

#### Database Architecture (Neon Serverless PostgreSQL)
- **Schema:** SQLModel-based schema definitions
- **Relationships:** User-task relationship with foreign keys
- **Indexing:** Optimized indexes for common queries
- **Security:** Row-level security for user data isolation

### Technology Stack Rationale

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Frontend | Next.js 16+ App Router | Modern React framework with SSR/SSG, built-in routing, excellent developer experience |
| Styling | Tailwind CSS | Utility-first CSS framework for rapid UI development |
| Backend | Python FastAPI | High-performance, easy-to-use framework with automatic API documentation |
| Database | Neon Serverless PostgreSQL | Serverless PostgreSQL with great performance and scalability |
| ORM | SQLModel | Combines SQLAlchemy and Pydantic with type hints |
| Auth | Better Auth | Modern authentication library with JWT support |
| Language | TypeScript | Type safety for frontend, improving maintainability |

### Data Flow

1. **User Registration/Login:**
   - User provides credentials to frontend
   - Frontend sends credentials to backend auth endpoint
   - Backend validates credentials and returns JWT
   - Frontend stores JWT for subsequent requests

2. **Task Operations:**
   - Frontend sends authenticated requests to backend API
   - Backend verifies JWT and extracts user ID
   - Backend enforces user ownership (URL user_id matches token user)
   - Backend performs CRUD operations on database
   - Backend returns JSON response to frontend
   - Frontend updates UI based on response

3. **Security Flow:**
   - All API requests include Authorization: Bearer <token>
   - Backend middleware validates JWT using BETTER_AUTH_SECRET
   - Backend middleware ensures user owns requested resources
   - Unauthorized requests return 401/403 status codes

### Deployment Architecture

- **Frontend:** Static hosting (Vercel, Netlify, or similar)
- **Backend:** Serverless or containerized deployment
- **Database:** Neon Serverless PostgreSQL cloud service
- **Environment:** Separate environments for development, staging, production

### Security Architecture

- **Transport Security:** HTTPS for all communications
- **Authentication:** JWT tokens with proper expiration
- **Authorization:** User ID validation on all requests
- **Input Validation:** Backend validation for all inputs
- **Database Security:** Row-level security through user_id foreign keys
- **Secrets Management:** Environment variables for sensitive data

### Performance Considerations

- **Frontend:** Code splitting, image optimization, caching strategies
- **Backend:** Async operations, database indexing, connection pooling
- **Database:** Proper indexing on user_id and completed fields
- **API:** Efficient query patterns, pagination for large datasets

### Scalability Considerations

- **Frontend:** Static asset optimization, CDN usage
- **Backend:** Stateless design, horizontal scaling capability
- **Database:** Serverless PostgreSQL scaling, read replicas if needed
- **Authentication:** JWT-based stateless authentication