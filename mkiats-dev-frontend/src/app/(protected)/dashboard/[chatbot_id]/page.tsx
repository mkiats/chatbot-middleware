'use client';

import { ChatbotViewForm } from '@/components/dashboard/chatbotViewForm';
import { Skeleton } from '@/components/ui/skeleton';
import { getChatbotById, updateChatbotById } from '@/lib/api';
import { Chatbot } from '@/lib/types/models';
import {
	GetChatbotByIdRequest,
	UpdateChatbotByIdRequest,
} from '@/lib/types/requests';
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';

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

const DashboardDetails = () => {
	const params = useParams();
	const chatbot_id = params.chatbot_id;
	const [chatbot, setChatbot] = useState<Chatbot | null>(null);
	const [isLoading, setIsLoading] = useState(true);
	const [isEditing, setIsEditing] = useState(false);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const fetchChatbot = async () => {
			try {
				if (chatbot_id) {
					const getChatbotByIdRequest: GetChatbotByIdRequest = {
						chatbot_id: chatbot_id.toString(),
					};
					const response = await getChatbotById(
						getChatbotByIdRequest,
					);
					if (response?.chatbots[0]) {
						setChatbot(response.chatbots[0]);
					} else {
						setError('Chatbot not found');
					}
				}
			} catch (err) {
				setError(
					err instanceof Error
						? err.message
						: 'Failed to fetch chatbot details',
				);
			} finally {
				setIsLoading(false);
			}
		};

		fetchChatbot();
	}, [chatbot_id]);

	const handleSubmit = async (chatbotData: Chatbot) => {
		try {
			if (!chatbot_id) {
				throw new Error('Chatbot ID is required');
			}
			const updateChatbotByIdRequest: UpdateChatbotByIdRequest = {
				chatbot_id: chatbot_id.toString(),
				chatbot_name: chatbotData.name,
				chatbot_version: chatbotData.version,
				chatbot_desc: chatbotData.description,
				chatbot_status: chatbotData.status,
				chatbot_telegram_support: chatbotData.telegram_support,
			};
			await updateChatbotById(updateChatbotByIdRequest);
			setIsEditing(false);
			window.location.reload();
		} catch (err) {
			setError(
				err instanceof Error ? err.message : 'Failed to update chatbot',
			);
			console.error('Error updating chatbot:', error);
		}
	};

	if (isLoading) {
		return <TableSkeleton />;
	}

	if (error) {
		return <div>Error: {error}</div>;
	}

	if (!chatbot) {
		return <div>No chatbot found</div>;
	}

	return (
		<div className='container mx-auto p-4'>
			<ChatbotViewForm
				chatbot={chatbot}
				onSubmit={handleSubmit}
				isEditing={isEditing}
				onEditToggle={() => setIsEditing(!isEditing)}
			/>
		</div>
	);
};

export default DashboardDetails;
