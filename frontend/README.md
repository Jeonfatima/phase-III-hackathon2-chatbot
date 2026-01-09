# Todo App Frontend

A sleek, modern, and responsive Next.js frontend for the Todo application with Better Auth integration.

## Features

- User authentication (signup, signin, signout)
- Task management (create, read, update, delete)
- Task completion toggling
- Responsive design for mobile and desktop
- Modern UI with Tailwind CSS
- JWT-based authentication with automatic token handling

## Tech Stack

- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Better Auth
- Node.js

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file with the following environment variables:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── (auth)/         # Authentication pages
│   │   ├── login/
│   │   └── register/
│   ├── (app)/          # Protected application pages
│   └── layout.tsx      # Root layout
├── components/         # Reusable UI components
│   ├── auth/          # Authentication components
│   ├── tasks/         # Task management components
│   └── ui/            # Base UI components
├── lib/               # Shared utilities and types
├── hooks/             # Custom React hooks
└── providers/         # React context providers
```

## Environment Variables

- `NEXT_PUBLIC_BETTER_AUTH_URL`: Base URL for the Better Auth service
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run linter

## API Integration

The frontend communicates with the backend through a centralized API client that automatically handles JWT token attachment and error responses.