# Quickstart Guide: Frontend UI + Better Auth Integration

## Prerequisites
- Node.js 18+ installed
- Access to the backend API with JWT authentication
- BETTER_AUTH_SECRET configured in backend
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Getting Started

### 1. Clone and Setup
```bash
# Navigate to the frontend directory
cd frontend/

# Install dependencies
npm install next react react-dom typescript @types/react @types/node @types/react-dom
npm install better-auth tailwindcss postcss autoprefixer
```

### 2. Initialize Tailwind CSS
```bash
npx tailwindcss init -p
```

### 3. Configure Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 4. Run the Development Server
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Key Features

### Authentication
- Visit `/auth/login` to sign in
- Visit `/auth/register` to create an account
- Authentication state is managed automatically
- JWT tokens are handled by Better Auth

### Task Management
- Access the dashboard at `/` (requires authentication)
- Create new tasks using the form
- View, edit, and delete existing tasks
- Toggle task completion status

## Project Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── layout.tsx
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (app)/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── layout.tsx
├── components/
│   ├── ui/
│   ├── auth/
│   └── tasks/
├── lib/
│   └── api.ts
├── hooks/
└── providers/
```

## API Integration
The frontend communicates with the backend through the centralized API client in `/lib/api.ts`:
- Automatically attaches JWT tokens
- Handles 401/403 responses
- Provides consistent error handling
- Implements loading states

## Development Commands
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run production server
npm start

# Run linting
npm run lint
```

## Next Steps
1. Customize the UI components to match your design requirements
2. Add additional pages as needed
3. Implement any additional features
4. Test across different browsers and devices
5. Deploy to your preferred hosting platform