import React from 'react';
import Link from 'next/link';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Todo App
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Sign in to your account or create a new one
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {children}
          <div className="mt-6 text-center">
            <Link
              href="/auth/login"
              className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
            >
              Login
            </Link>
            <span className="mx-2 text-gray-400">|</span>
            <Link
              href="/auth/register"
              className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
            >
              Register
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};