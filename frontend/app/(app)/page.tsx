'use client';

import React from 'react';
import { TaskList } from '@/components/tasks/task-list';
import { TaskForm } from '@/components/tasks/task-form';
import { useTasks } from '@/hooks/use-tasks';
import { useAuth } from '@/providers/auth-provider';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { tasks: filteredTasks, createTask, loading, error, setFilter, filter } = useTasks();
  const { logout } = useAuth();
  const router = useRouter();

  const handleCreateTask = async (title: string, description: string) => {
    await createTask(title, description);
  };

  const handleSignOut = async () => {
    await logout();
    router.push('/(auth)/login');
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
        <div className="flex space-x-4">
          <Button variant="secondary" size="sm" onClick={handleSignOut}>
            Sign Out
          </Button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </div>
      )}

      <TaskForm onSubmit={handleCreateTask} loading={loading} />

      <div className="mt-8">
        <div className="flex space-x-4 mb-4">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-md text-sm font-medium ${
              filter === 'all'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('active')}
            className={`px-3 py-1 rounded-md text-sm font-medium ${
              filter === 'active'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Active
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1 rounded-md text-sm font-medium ${
              filter === 'completed'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Completed
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-32">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-indigo-600"></div>
          </div>
        ) : (
          <TaskList tasks={filteredTasks} />
        )}
      </div>
    </div>
  );
}