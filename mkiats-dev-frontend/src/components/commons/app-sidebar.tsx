'use client';
import * as React from 'react';

import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarGroup,
	SidebarGroupContent,
	SidebarGroupLabel,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	SidebarRail,
} from '@/components/ui/sidebar';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
	LayoutDashboardIcon,
	RocketIcon,
	BookOpenIcon,
	CloudUploadIcon,
	LogOutIcon,
} from 'lucide-react';
import { ModeToggle } from './dark-mode-toggle';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/lib/contexts/AuthContext';

// This is sample data.
const data = {
	navMain: [
		{
			title: 'Main',
			url: '',
			items: [
				{
					title: 'Dashboard',
					url: '/dashboard',
				},
				{
					title: 'Deployment',
					url: '/deployment',
				},
				{
					title: 'Documentation',
					url: '/documentation',
				},
			],
		},
	],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
	const { logout, developerName } = useAuth();
	const pathname = usePathname();
	const isActiveRoute = (url: string): boolean => {
		// Handle both absolute and relative URLs
		const normalizedUrl = url.startsWith('/') ? url : `/${url}`;
		return pathname === normalizedUrl;
	};

	return (
		<Sidebar {...props}>
			<SidebarHeader className='flex h-16 mt-4'>
				<span className='flex h-full justify-center items-center font-serif font-bold gap-2 text-accent-foreground text-xl'>
					<CloudUploadIcon />
					Elunify
				</span>
				{/* <SearchForm />  */}
			</SidebarHeader>
			<SidebarContent className='gap-8'>
				{/* We create a SidebarGroup for each parent. */}
				{data.navMain.map((item) => (
					<SidebarGroup key={item.title}>
						<SidebarGroupLabel className='h-12 bg-secondary text-md font-extrabold text-secondary-foreground pl-4 mb-2'>
							{item.title}
						</SidebarGroupLabel>
						<SidebarGroupContent>
							<SidebarMenu>
								{item.items.map((item) => (
									<SidebarMenuItem
										key={item.title}
										className='h-12'
									>
										<SidebarMenuButton
											asChild
											isActive={isActiveRoute(item.url)}
											className='h-full'
										>
											<Link
												href={item.url}
												key={item.title}
											>
												{item.title === 'Dashboard' && (
													<LayoutDashboardIcon />
												)}
												{item.title ===
													'Deployment' && (
													<RocketIcon />
												)}
												{item.title ===
													'Documentation' && (
													<BookOpenIcon />
												)}
												{item.title}
											</Link>
										</SidebarMenuButton>
									</SidebarMenuItem>
								))}
							</SidebarMenu>
						</SidebarGroupContent>
					</SidebarGroup>
				))}
			</SidebarContent>
			<SidebarFooter className='mb-4'>
				<>
					<ModeToggle />
					<Card className='h-24 flex items-center px-2 bg-background'>
						<span className='w-4/5 text-sm font-medium truncate text-foreground ml-4'>
							{developerName}
						</span>
						<span className='w-1/5'>
							<Button
								variant='ghost'
								size='icon'
								className='h-12 w-12'
								onClick={logout}
							>
								<LogOutIcon />
							</Button>
						</span>
					</Card>
				</>
			</SidebarFooter>
			<SidebarRail />
		</Sidebar>
	);
}
