// frontend/hooks/use-tasks.ts

import { useEffect, useState } from "react";
import { apiClient, Task } from "@/lib/api";
import { useAuth } from "@/providers/auth-provider";

type Filter = "all" | "active" | "completed";

// Helper function to safely extract error message
const extractErrorMessage = (errorObj: any, defaultMessage: string = "An error occurred"): string => {
  if (!errorObj) return defaultMessage;

  // If it's already a string, return it
  if (typeof errorObj === 'string') return errorObj;

  // If it has a message property, return that
  if (errorObj.message) return errorObj.message;

  // If it has a detail property, return that
  if (errorObj.detail) return errorObj.detail;

  // If it's an array (like validation errors), join the messages
  if (Array.isArray(errorObj)) {
    return errorObj.map(err =>
      typeof err === 'string' ? err :
      err.msg || err.detail || err.message || JSON.stringify(err)
    ).join('; ');
  }

  // Fallback to string conversion
  return String(errorObj);
};

export const useTasks = () => {
  const { token, user } = useAuth();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<Filter>("all");

  useEffect(() => {
    if (token && user?.id) {
      loadTasks();
    }
  }, [token, user]);

  const loadTasks = async () => {
    if (!token || !user?.id) return;

    setLoading(true);
    setError(null);

    const res = await apiClient.getTasks(user.id, token);

    if (res.success && Array.isArray(res.data)) {
      const tasksData = [...res.data];
      setTasks(() => tasksData);
    } else {
      setError(extractErrorMessage(res.error, "Failed to load tasks"));
    }

    setLoading(false);
  };

  const createTask = async (title: string, description?: string) => {
    if (!token || !user?.id) return;

    setLoading(true);
    setError(null);

    const res = await apiClient.createTask(
      user.id,
      { title, description, completed: false },
      token
    );

    if (res.success && res.data) {
      const newTask = res.data;
      setTasks(prev => [...prev, newTask]);
    } else {
      setError(extractErrorMessage(res.error, "Failed to create task"));
    }

    setLoading(false);
  };

  const updateTask = async (taskId: number, data: Partial<Task>) => {
    if (!token || !user?.id) return;

    setLoading(true);
    setError(null);

    const res = await apiClient.updateTask(user.id, taskId, data, token);

    if (!res.success || !res.data) {
      setError(extractErrorMessage(res.error, "Failed to update task"));
      setLoading(false);
      return;
    }

    const updatedTask = res.data;

    setTasks(prev =>
      prev.map(task =>
        task.id === taskId ? updatedTask : task
      )
    );

    setLoading(false);
  };

  const deleteTask = async (taskId: number) => {
    if (!token || !user?.id) return;

    setLoading(true);
    setError(null);

    const res = await apiClient.deleteTask(user.id, taskId, token);

    if (res.success) {
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } else {
      setError(extractErrorMessage(res.error, "Failed to delete task"));
    }

    setLoading(false);
  };

  const toggleTaskCompletion = async (taskId: number) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task || !token || !user?.id) return;

    setLoading(true);
    setError(null);

    const res = await apiClient.toggleTaskCompletion(user.id, taskId, !task.completed, token);

    if (!res.success || !res.data) {
      setError(extractErrorMessage(res.error, "Failed to toggle task completion"));
      setLoading(false);
      return;
    }

    const updatedTask = res.data;

    setTasks(prev =>
      prev.map(task =>
        task.id === taskId ? updatedTask : task
      )
    );

    setLoading(false);
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === "active") return !task.completed;
    if (filter === "completed") return task.completed;
    return true;
  });

  return {
    tasks: filteredTasks,
    loading,
    error,
    filter,
    setFilter,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    reload: loadTasks,
  };
};
