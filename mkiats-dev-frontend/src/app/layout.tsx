import type { Metadata } from 'next';
import localFont from 'next/font/local';
import './globals.css';
// import { ThemeProvider } from '@/components/commons/theme-provider';
// import { ModeToggle } from '@/components/commons/dark-mode-toggle';
// import { CloudAlertIcon, LucideCloudUpload } from 'lucide-react';
// import { AppSidebar } from '@/components/commons/app-sidebar';
// import {
// 	Breadcrumb,
// 	BreadcrumbItem,
// 	BreadcrumbLink,
// 	BreadcrumbList,
// 	BreadcrumbPage,
// 	BreadcrumbSeparator,
// } from '@/components/ui/breadcrumb';
// import { Separator } from '@/components/ui/separator';
// import {
// 	SidebarInset,
// 	SidebarProvider,
// 	SidebarTrigger,
// } from '@/components/ui/sidebar';
// import { AuthProvider } from '@/lib/contexts/AuthContext';
// import ProtectedLayout from '@/components/commons/protected-layout';

require('dotenv').config();
const geistSans = localFont({
	src: './fonts/GeistVF.woff',
	variable: '--font-geist-sans',
	weight: '100 900',
});
const geistMono = localFont({
	src: './fonts/GeistMonoVF.woff',
	variable: '--font-geist-mono',
	weight: '100 900',
});

export const metadata: Metadata = {
	title: 'Elunify',
	description:
		'Interface built to streamline chatbot monitoring and deployment',
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang='en' suppressHydrationWarning>
			<body
				className={`${geistSans.variable} ${geistMono.variable} antialiased`}
			>
				{children}
			</body>
		</html>
	);
}
