'use client';

import React from 'react';
import { RegisterForm } from '@/components/auth/register-form';
import { useAuthState } from '@/hooks/use-auth';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const { handleRegister, registerForm, setRegisterForm, isAuthenticated } = useAuthState();
  const router = useRouter();

  // Redirect to dashboard if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, router]);

  const updateForm = (field: string, value: string | boolean) => {
    setRegisterForm(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  return (
    <div>
      <RegisterForm
        email={registerForm.email}
        password={registerForm.password}
        confirmPassword={registerForm.confirmPassword}
        error={registerForm.error}
        loading={registerForm.loading}
        onEmailChange={(value) => updateForm('email', value)}
        onPasswordChange={(value) => updateForm('password', value)}
        onConfirmPasswordChange={(value) => updateForm('confirmPassword', value)}
        onSubmit={handleRegister}
      />
    </div>
  );
}