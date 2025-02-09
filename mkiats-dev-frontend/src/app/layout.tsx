import type { Metadata } from 'next';
import localFont from 'next/font/local';
import './globals.css';
import { ThemeProvider } from '@/components/commons/theme-provider';
import Navbar from '@/components/commons/navbar';
import { ModeToggle } from '@/components/commons/dark-mode-toggle';

import { AppSidebar } from '@/components/app-sidebar';
import {
	Breadcrumb,
	BreadcrumbItem,
	BreadcrumbLink,
	BreadcrumbList,
	BreadcrumbPage,
	BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import { Separator } from '@/components/ui/separator';
import {
	SidebarInset,
	SidebarProvider,
	SidebarTrigger,
} from '@/components/ui/sidebar';

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
	title: 'Ez Deploy',
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
				<ThemeProvider
					attribute='class'
					defaultTheme='light'
					enableSystem
					disableTransitionOnChange
				>
					<section className='w-screen h-screen'>
						<SidebarProvider>
							<AppSidebar />
							<SidebarInset>
								<header className='hidden w-full h-16 bg-transparent grid grid-cols-3 justify-center'>
									{/* <div className='col-start-2 flex justify-center items-center gap-8 '>
										<Navbar />
									</div> */}
								</header>
								<header className='flex h-16 shrink-0 items-center gap-2 border-b px-4'>
									<SidebarTrigger className='-ml-1' />
									<Separator
										orientation='vertical'
										className='mr-2 h-4'
									/>
									{/* <Breadcrumb>
										<BreadcrumbList>
											<BreadcrumbItem className='hidden md:block'>
												<BreadcrumbLink href='#'>
													Building Your Application
												</BreadcrumbLink>
											</BreadcrumbItem>
											<BreadcrumbSeparator className='hidden md:block' />
											<BreadcrumbItem>
												<BreadcrumbPage>
													Data Fetching
												</BreadcrumbPage>
											</BreadcrumbItem>
										</BreadcrumbList>
									</Breadcrumb> */}
									<div className='flex justify-self-end items-center pr-4'>
										<ModeToggle />
									</div>
								</header>
								<div className='w-full h-[calc(100vh-4rem)] flex-col gap-4 p-4'>
									{children}
								</div>
							</SidebarInset>
						</SidebarProvider>
					</section>
				</ThemeProvider>
			</body>
		</html>
	);
}
