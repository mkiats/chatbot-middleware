'use client';

import { getAllChatbots, getChatbotsByDeveloperId } from '@/lib/api';
import { columns } from '../../../components/dashboard/columns';
import { DataTable } from '../../../components/dashboard/data-table';
import { Chatbot } from '@/lib/types/models';
import { useEffect, useState } from 'react';
import { Skeleton } from '@/components/ui/skeleton';
import { useAuth } from '@/lib/contexts/AuthContext';
import { GetChatbotsByDeveloperIdRequest } from '@/lib/types/requests';

function TableSkeleton() {
	return (
		<div className='space-y-3'>
			{/* Table Rows Skeleton */}
			{[1, 2, 3, 4, 5].map((index) => (
				<Skeleton className='h-8 w-full' key={index} />
			))}
		</div>
	);
}

function DashboardPage() {
	const { developerUuid } = useAuth();
	const [chatbots, setChatbots] = useState<Chatbot[]>([]);
	const [isLoading, setIsLoading] = useState(true);
	const [error, setError] = useState<Error | null>(null);

	const fetchChatbots = async () => {
		try {
			setIsLoading(true);
			const getChatbotsByDeveloperIdRequest: GetChatbotsByDeveloperIdRequest = {developer_id: developerUuid!}
			const response = await getChatbotsByDeveloperId(getChatbotsByDeveloperIdRequest);
			setChatbots(response.chatbots);
		} catch (err) {
			setError(
				err instanceof Error
					? err
					: new Error('Failed to fetch chatbots'),
			);
			console.error('Error fetching chatbots:', err);
		} finally {
			setIsLoading(false);
		}
	};

	useEffect(() => {
		fetchChatbots();
	}, []);

	if (isLoading) {
		return (
			<div className='container mx-auto py-10'>
				<TableSkeleton />
			</div>
		);
	}

	if (error) {
		return (
			<div className='container mx-auto py-10'>
				<div className='text-red-500'>Error: {error.message}</div>
			</div>
		);
	}

	return (
		<div className='container mx-auto py-10'>
			<DataTable
				columns={columns}
				data={chatbots}
				refreshHandler={fetchChatbots}
			/>
		</div>
	);
}

export default DashboardPage;
