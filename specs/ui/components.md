# UI Components Specification

## Component Overview

The UI components follow a modular, reusable approach using React with TypeScript and Tailwind CSS. Components are organized by functionality and purpose to ensure consistency and maintainability across the application.

## Component Categories

### 1. Layout Components

#### Header
- **Purpose:** Top navigation bar with branding and user controls
- **Props:**
  - `title?: string` - Optional page title to display
  - `showUserMenu?: boolean` - Whether to show user profile menu
- **Features:**
  - App logo/branding
  - Page title display
  - User profile dropdown with logout
  - Responsive design for mobile
- **Styling:** Fixed top position, shadow, responsive padding

#### Sidebar
- **Purpose:** Navigation sidebar for application sections
- **Props:**
  - `navigationItems: NavigationItem[]` - Array of navigation links
  - `isCollapsed?: boolean` - Whether sidebar is collapsed
- **Features:**
  - Navigation links with icons
  - Active state highlighting
  - Collapsible on mobile
- **Styling:** Fixed width, background contrast, smooth transitions

#### MainContent
- **Purpose:** Main content container with consistent padding
- **Props:**
  - `children: React.ReactNode` - Content to display
  - `className?: string` - Additional CSS classes
- **Features:**
  - Responsive padding
  - Max-width constraints
  - Scrollable content area
- **Styling:** Responsive padding, centered content, scrollable

### 2. Form Components

#### InputField
- **Purpose:** Standardized text input with validation
- **Props:**
  - `label: string` - Input label
  - `id: string` - Input ID for accessibility
  - `type?: string` - Input type (text, email, password, etc.)
  - `value: string` - Current input value
  - `onChange: (value: string) => void` - Change handler
  - `error?: string` - Error message to display
  - `required?: boolean` - Whether field is required
- **Features:**
  - Accessible labels
  - Error state styling
  - Required field indicators
- **Styling:** Consistent padding, border, focus states

#### TextArea
- **Purpose:** Multi-line text input with validation
- **Props:**
  - `label: string` - Textarea label
  - `id: string` - Textarea ID for accessibility
  - `value: string` - Current textarea value
  - `onChange: (value: string) => void` - Change handler
  - `error?: string` - Error message to display
  - `placeholder?: string` - Placeholder text
  - `rows?: number` - Number of visible text rows
- **Features:**
  - Resizable by default
  - Accessible labels
  - Error state styling
- **Styling:** Consistent padding, border, focus states

#### Button
- **Purpose:** Standardized button with different variants
- **Props:**
  - `children: React.ReactNode` - Button content
  - `variant?: 'primary' | 'secondary' | 'danger' | 'outline'` - Button style
  - `size?: 'sm' | 'md' | 'lg'` - Button size
  - `type?: 'button' | 'submit' | 'reset'` - Button type
  - `disabled?: boolean` - Whether button is disabled
  - `onClick?: () => void` - Click handler
  - `fullWidth?: boolean` - Whether button takes full width
- **Features:**
  - Multiple style variants
  - Loading state support (future)
  - Accessible button types
- **Styling:** Consistent padding, border, hover states

#### Checkbox
- **Purpose:** Standardized checkbox input
- **Props:**
  - `label: string` - Checkbox label
  - `checked: boolean` - Current checked state
  - `onChange: (checked: boolean) => void` - Change handler
  - `id?: string` - Checkbox ID for accessibility
- **Features:**
  - Accessible labels
  - Visual checked state
  - Consistent styling
- **Styling:** Custom checkbox appearance, focus states

### 3. Task Components

#### TaskCard
- **Purpose:** Display a single task with interactive elements
- **Props:**
  - `task: Task` - Task object to display
  - `onToggleComplete?: (id: number, completed: boolean) => void` - Completion toggle handler
  - `onEdit?: (id: number) => void` - Edit handler
  - `onDelete?: (id: number) => void` - Delete handler
- **Features:**
  - Title display with completion strikethrough
  - Description display (if available)
  - Completion status toggle
  - Edit and delete buttons
  - Visual indication of completion status
- **Styling:** Card layout, hover effects, completion styling

#### TaskForm
- **Purpose:** Form for creating or editing tasks
- **Props:**
  - `initialData?: Partial<Task>` - Initial form data
  - `onSubmit: (taskData: Omit<Task, 'id' | 'created_at' | 'updated_at'>) => void` - Submit handler
  - `onCancel?: () => void` - Cancel handler
  - `submitLabel?: string` - Label for submit button
- **Features:**
  - Title input with validation
  - Description textarea
  - Completion status toggle
  - Form validation
  - Loading state during submission
- **Styling:** Form layout, consistent spacing, error states

#### TaskList
- **Purpose:** Display multiple tasks with filtering options
- **Props:**
  - `tasks: Task[]` - Array of tasks to display
  - `onToggleComplete?: (id: number, completed: boolean) => void` - Completion toggle handler
  - `onEdit?: (id: number) => void` - Edit handler
  - `onDelete?: (id: number) => void` - Delete handler
  - `filter?: 'all' | 'active' | 'completed'` - Filter status
  - `onFilterChange?: (filter: 'all' | 'active' | 'completed') => void` - Filter change handler
- **Features:**
  - Task cards display
  - Filtering controls
  - Empty state handling
  - Loading state during data fetch
- **Styling:** List layout, responsive grid, filter controls

### 4. Authentication Components

#### LoginForm
- **Purpose:** Form for user login
- **Props:**
  - `onLogin: (email: string, password: string) => void` - Login handler
  - `loading?: boolean` - Whether login is in progress
- **Features:**
  - Email input with validation
  - Password input with visibility toggle
  - Form validation
  - Loading state during authentication
- **Styling:** Form layout, consistent spacing, loading states

#### RegisterForm
- **Purpose:** Form for user registration
- **Props:**
  - `onRegister: (email: string, password: string) => void` - Registration handler
  - `loading?: boolean` - Whether registration is in progress
- **Features:**
  - Email input with validation
  - Password input with strength indicator
  - Confirm password input
  - Form validation
  - Password strength feedback
- **Styling:** Form layout, consistent spacing, strength indicator

#### AuthLayout
- **Purpose:** Layout wrapper for authentication pages
- **Props:**
  - `children: React.ReactNode` - Content to display
  - `title: string` - Page title
- **Features:**
  - Centered form container
  - App branding
  - Responsive design
- **Styling:** Centered container, consistent spacing, responsive

### 5. Data Display Components

#### LoadingSpinner
- **Purpose:** Visual indicator for loading states
- **Props:**
  - `size?: 'sm' | 'md' | 'lg'` - Spinner size
  - `label?: string` - Optional loading label
- **Features:**
  - Animated spinner
  - Accessible loading state
  - Multiple size options
- **Styling:** Animated spinner, consistent sizing

#### EmptyState
- **Purpose:** Display message when no data is available
- **Props:**
  - `icon?: React.ReactNode` - Optional icon to display
  - `title: string` - Title of empty state
  - `description?: string` - Description of empty state
  - `action?: React.ReactNode` - Optional action button
- **Features:**
  - Visual icon or illustration
  - Descriptive text
  - Optional call-to-action
- **Styling:** Centered content, visual hierarchy

#### Alert
- **Purpose:** Display important messages to the user
- **Props:**
  - `type: 'info' | 'success' | 'warning' | 'error'` - Alert type
  - `message: string` - Alert message
  - `title?: string` - Optional alert title
  - `onClose?: () => void` - Close handler (optional)
- **Features:**
  - Different visual styles per type
  - Optional close button
  - Accessible notifications
- **Styling:** Color-coded backgrounds, consistent padding

### 6. Navigation Components

#### Breadcrumb
- **Purpose:** Show current page location in site hierarchy
- **Props:**
  - `items: BreadcrumbItem[]` - Array of breadcrumb items
- **Features:**
  - Link navigation
  - Current page indication
  - Responsive design
- **Styling:** Horizontal layout, separators, current page styling

#### Pagination
- **Purpose:** Navigate through paginated content
- **Props:**
  - `currentPage: number` - Current page number
  - `totalPages: number` - Total number of pages
  - `onPageChange: (page: number) => void` - Page change handler
- **Features:**
  - Previous/next buttons
  - Page number buttons
  - Current page indication
- **Styling:** Button group layout, active state

## Component Reusability Guidelines

### Naming Convention:
- Use PascalCase for component names
- Prefix with category when appropriate (AuthLoginForm, TaskCard)
- Use descriptive names that indicate purpose

### Prop Interface:
- Define TypeScript interfaces for complex prop types
- Use optional props with default values when appropriate
- Include JSDoc comments for all props

### Styling Approach:
- Use Tailwind CSS utility classes
- Create reusable CSS classes for common patterns
- Avoid inline styles except for dynamic values

### Accessibility:
- Include proper ARIA attributes
- Ensure keyboard navigation support
- Use semantic HTML elements
- Provide alternative text for images

## Component Dependencies

### External Dependencies:
- **React:** Core component library
- **TypeScript:** Type checking
- **Tailwind CSS:** Styling framework
- **Better Auth:** Authentication components
- **Next.js:** Router and navigation components

### Internal Dependencies:
- Components should be self-contained when possible
- Shared components in common directory
- Specific components in feature directories
- Component composition over inheritance