import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { ChatbotFormData } from './chatbotDetailsForm';

interface ChatbotDetailsValidationProps {
	formData: ChatbotFormData;
	onBack: () => void;
	onConfirm: () => void;
	title?: string;
}

const ChatbotDetailsValidation: React.FC<ChatbotDetailsValidationProps> = ({
	formData,
	onBack,
	onConfirm,
	title = 'Review Chatbot Configuration',
}) => {
	// Helper function to format field names
	const formatFieldName = (name: string) => {
		return name
			.split('_')
			.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
			.join(' ');
	};

	// Helper function to render field value based on type
	const renderFieldValue = (value: any) => {
		if (typeof value === 'boolean') {
			return value ? 'Yes' : 'No';
		}
		if (value === undefined || value === '') {
			return 'N.A';
		}
		return value;
	};

	// Filter and group fields based on deployment type
	const renderFields = () => {
		const baseFields = [
			'name',
			'version',
			'description',
			'status',
			'telegram_support',
		];
		const deploymentFields = Object.keys(formData).filter(
			(key) => !baseFields.includes(key) && key !== 'deployment_type',
		);

		return (
			<section className='flex flex-col gap-8'>
				{/* Base Information */}
				<Card>
					<CardHeader>
						<CardTitle>Basic Information</CardTitle>
					</CardHeader>
					<CardContent className='grid gap-4'>
						{baseFields.map((field) => (
							<div
								key={field}
								className='grid grid-cols-2 gap-4 items-center'
							>
								<span className='font-medium'>
									{formatFieldName(field)}
								</span>
								<span>
									{renderFieldValue(
										formData[
											field as keyof ChatbotFormData
										],
									)}
								</span>
							</div>
						))}
					</CardContent>
				</Card>

				{/* Deployment Information */}
				<Card>
					<CardHeader>
						<CardTitle>Deployment Configuration</CardTitle>
					</CardHeader>
					<CardContent className='grid gap-4'>
						<div className='grid grid-cols-2 gap-4 items-center'>
							<span className='font-medium'>Deployment Type</span>
							<span className='capitalize'>
								{formData.deployment_type}
							</span>
						</div>
						{deploymentFields.map((field) => (
							<div
								key={field}
								className='grid grid-cols-2 gap-4 items-center'
							>
								<span className='font-medium'>
									{formatFieldName(field)}
								</span>
								<span>
									{renderFieldValue(
										formData[
											field as keyof ChatbotFormData
										],
									)}
								</span>
							</div>
						))}
					</CardContent>
				</Card>
			</section>
		);
	};

	return (
		<>
			<ScrollArea className='h-full pr-4'>
				<div className='text-2xl font-bold'>{title}</div>
				{renderFields()}
				<div className='flex justify-between pt-6'>
					<Button
						variant='outline'
						onClick={onBack}
						className='w-[200px]'
					>
						Back to Edit
					</Button>
					<Button onClick={onConfirm} className='w-[200px]'>
						Confirm & Continue
					</Button>
				</div>
			</ScrollArea>
		</>
	);
};

export default ChatbotDetailsValidation;
