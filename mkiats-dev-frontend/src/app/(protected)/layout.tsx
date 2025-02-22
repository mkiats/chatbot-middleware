// app/(protected)/layout.tsx
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/commons/app-sidebar';
import { Separator } from '@/components/ui/separator';
import { SidebarTrigger } from '@/components/ui/sidebar';
import { ThemeProvider } from '@/components/commons/theme-provider';
import { AuthProvider } from '@/lib/contexts/AuthContext';
import ProtectedLayout from '@/components/commons/protected-layout';

export default function ProtectedPagesLayout({
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
        <ProtectedLayout>
          <section className='w-screen h-screen'>
            <SidebarProvider>
              <AppSidebar />
              <SidebarInset>
                <header className='flex h-16 shrink-0 items-center gap-2 border-b px-4'>
                  <SidebarTrigger className='-ml-1' />
                  <Separator orientation='vertical' className='mr-2 h-4' />
                </header>
                <div className='w-full h-[calc(100vh-4rem)] flex-col gap-4 p-4'>
                  {children}
                </div>
              </SidebarInset>
            </SidebarProvider>
          </section>
        </ProtectedLayout>
      </AuthProvider>
    </ThemeProvider>
  );
}