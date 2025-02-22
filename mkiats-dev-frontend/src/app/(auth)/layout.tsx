import { ThemeProvider } from '@/components/commons/theme-provider';
import { AuthProvider } from '@/lib/contexts/AuthContext';

export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ThemeProvider
      attribute='class'
      defaultTheme='light'
      enableSystem
      disableTransitionOnChange
    >
      <AuthProvider>
        <main className="min-h-screen flex items-center justify-center">
          {children}
        </main>
      </AuthProvider>
    </ThemeProvider>
  );
}