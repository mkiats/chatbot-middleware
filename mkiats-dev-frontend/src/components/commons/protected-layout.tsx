// components/ProtectedLayout.tsx
'use client';

import { useAuth } from '@/lib/contexts/AuthContext';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect } from 'react';

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!loading && !isAuthenticated && pathname !== '/login') {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router, pathname]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated && pathname !== '/login') {
    return null;
  }

  return children;
}