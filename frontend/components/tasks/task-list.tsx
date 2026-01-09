import React from 'react';
import { Task } from '@/lib/types';
import { TaskCard } from './task-card';
import { EmptyState } from './empty-state';

interface TaskListProps {
  tasks?: Task[]; // Make tasks optional
}

export const TaskList: React.FC<TaskListProps> = ({ tasks }) => {
  // Safe check for undefined or empty array
  if (!tasks || tasks.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
};
