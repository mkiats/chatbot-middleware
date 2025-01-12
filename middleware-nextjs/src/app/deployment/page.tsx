'use client';
import {
	ChatbotCreationForm,
	ChatbotFormData,
} from '@/components/deployment/chatbotCreationForm';
import ChatbotCreationFormValidation from '@/components/deployment/chatbotCreationFormValidation';
import Stepper from '@/components/deployment/stepper';
import { TermsAndConditions } from '@/components/deployment/termsAndConditions';
import { Skeleton } from '@/components/ui/skeleton';
import { deployChatbot } from '@/lib/api';
import { DeployChatbotRequest } from '@/lib/types/requests';
import { DeployChatbotResponse } from '@/lib/types/responses';
import { useState } from 'react';

const DeploymentPage: React.FC = () => {
	const [currentStep, setCurrentStep] = useState<number>(1);
	const [formData, setFormData] = useState<ChatbotFormData | null>(null);
	const [isLoading, setIsLoading] = useState<boolean>(false);
	const [deploymentMessage, setDeploymentMessage] =
		useState<DeployChatbotResponse>();

	const stepList = [
		'Terms & Conditions',
		'Chatbot configurations',
		'Review',
		'Deployment',
	];

	const handleAcceptTermsAndConditions = (): void => {
		setCurrentStep(2);
	};

	const handleFormSubmit = (data: ChatbotFormData): void => {
		setFormData(data);
		setCurrentStep(3);
	};

	const handleValidationBack = (): void => {
		setCurrentStep(2);
	};

	const handleValidationNext = async (): Promise<void> => {
		setCurrentStep(4);
		if (formData) {
			setIsLoading(true);
			try {
				const deployChatbotRequest: DeployChatbotRequest = {
					chatbotFormData: formData,
				};
				const theDeploymentMessage =
					await deployChatbot(deployChatbotRequest);
				setDeploymentMessage(theDeploymentMessage);
			} finally {
				setIsLoading(false);
			}
		}
	};

	return (
		<div className='container h-full mx-auto px-4 py-8'>
			<div className='h-1/6'>
				<Stepper currentStep={currentStep} stepList={stepList} />
			</div>

			<div className='h-5/6'>
				{currentStep === 1 && (
					<TermsAndConditions
						onAccept={handleAcceptTermsAndConditions}
					/>
				)}

				{currentStep === 2 && (
					<ChatbotCreationForm onSubmit={handleFormSubmit} />
				)}

				{currentStep === 3 && formData && (
					<ChatbotCreationFormValidation
						formData={formData}
						onConfirm={handleValidationNext}
						onBack={handleValidationBack}
						title=''
					/>
				)}
				{currentStep === 4 && (
					<div className='w-full flex justify-center items-start'>
						{isLoading ? (
							<Skeleton className='w-3/4 h-[20px] rounded-full' />
						) : (
							<p className='text-sm text-gray-600'>
								{deploymentMessage?.message}
							</p>
						)}
					</div>
				)}
			</div>
		</div>
	);
};

export default DeploymentPage;
