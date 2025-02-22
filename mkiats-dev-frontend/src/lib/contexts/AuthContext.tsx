"use client"

import { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (developer_uuid: string, developer_name: string) => void;
  logout: () => void;
  loading: boolean;
  developerUuid: string | null;
  developerName: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [developerUuid, setDeveloperUuid] = useState<string | null>(null);
  const [developerName, setDeveloperName] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Check for developer UUID on mount
    const storedUuid = localStorage.getItem('developer_uuid');
    const storedName = localStorage.getItem('developer_name');
    if (storedUuid) {
      setDeveloperUuid(storedUuid);
      setIsAuthenticated(true);
    }
    if (storedName) {
      setDeveloperName(storedName);
    }
    setLoading(false);
  }, []);

  const login = (developer_uuid: string, developer_name: string) => {
    localStorage.setItem('developer_uuid', developer_uuid);
    localStorage.setItem('developer_name', developer_name);
    setDeveloperUuid(developer_uuid);
    setDeveloperName(developer_name);
    setIsAuthenticated(true);
    router.push('/dashboard');
  };

  const logout = () => {
    localStorage.removeItem('developer_uuid');
    localStorage.removeItem('developer_name');
    setDeveloperUuid(null);
    setDeveloperName(null);
    setIsAuthenticated(false);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ 
      isAuthenticated, 
      login, 
      logout, 
      loading,
      developerUuid,
      developerName
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};