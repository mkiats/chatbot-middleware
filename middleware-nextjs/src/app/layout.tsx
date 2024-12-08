import type { Metadata } from 'next';
import localFont from 'next/font/local';
import './globals.css';
import { ThemeProvider } from '@/components/theme-provider';
import Navbar from '@/components/navbar';
import { ModeToggle } from '@/components/dark-mode-toggle';

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
					<header className='w-screen h-24 bg-transparent grid grid-cols-3 justify-center'>
						<div className='col-start-2 flex justify-center items-center gap-8 '>
							<Navbar />
						</div>
						<div className='col-start-3 flex justify-self-end items-center pr-4'>
							<ModeToggle />
						</div>
					</header>
					<section className='w-screen h-[calc(100vh-6rem)] overflow-y-auto'>
						{children}
					</section>
				</ThemeProvider>
			</body>
		</html>
	);
}
