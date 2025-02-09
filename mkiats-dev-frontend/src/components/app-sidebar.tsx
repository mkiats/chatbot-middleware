'use client';
import * as React from 'react';

import { SearchForm } from '@/components/search-form';
import { VersionSwitcher } from '@/components/version-switcher';
import {
	Sidebar,
	SidebarContent,
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

// This is sample data.
const data = {
	versions: ['1.0.1', '1.1.0-alpha', '2.0.0-beta1'],
	navMain: [
		{
			title: 'Getting Started',
			url: '#',
			items: [
				{
					title: 'Documentation',
					url: '#',
				},
				{
					title: 'FYP Explanation',
					url: '#',
				},
			],
		},
		{
			title: 'Modules',
			url: '',
			items: [
				{
					title: 'Dashboard',
					url: '/dashboard',
				},
				{
					title: 'Deployment',
					url: '/deployment',
				}
			],
		},
	],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
	const pathname = usePathname();
	const isActiveRoute = (url: string): boolean => {
		// Handle both absolute and relative URLs
		const normalizedUrl = url.startsWith('/') ? url : `/${url}`;
		return pathname === normalizedUrl;
	};

	return (
		<Sidebar {...props}>
			<SidebarHeader>
				{/* <VersionSwitcher
          versions={data.versions}
          defaultVersion={data.versions[0]}
        />
        <SearchForm /> */}
			</SidebarHeader>
			<SidebarContent>
				{/* We create a SidebarGroup for each parent. */}
				{data.navMain.map((item) => (
					<SidebarGroup key={item.title}>
						<SidebarGroupLabel className='bg-secondary text-secondary-foreground'>
							{item.title}
						</SidebarGroupLabel>
						<SidebarGroupContent>
							<SidebarMenu>
								{item.items.map((item) => (
									<SidebarMenuItem key={item.title}>
										<SidebarMenuButton
											asChild
											isActive={isActiveRoute(item.url)}
										>
											<Link
												href={item.url}
												key={item.title}
											>
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
			<SidebarRail />
		</Sidebar>
	);
}
