'use client';
import {
	ChatbotCreationForm,
	ChatbotFormData,
} from '@/components/deployment/chatbotCreationForm';
import ChatbotCreationFormValidation from '@/components/deployment/chatbotCreationFormValidation';
import Stepper from '@/components/deployment/stepper';
import { TermsAndConditions } from '@/components/deployment/termsAndConditions';
import { CheckCircle, Loader2 } from 'lucide-react';
import {
	deployApplication,
	deployInfrastructure,
	validateDeployment,
} from '@/lib/api';
import { DeployChatbotRequest } from '@/lib/types/requests';
import { useState, useEffect } from 'react';
import { useInfrastructurePolling } from '@/lib/hooks/useTerraformPolling';
import { DeploymentMessage, TerraformStatus } from '@/lib/types/models';

const DeploymentPage: React.FC = () => {
	const [currentStep, setCurrentStep] = useState<number>(1);
	const [formData, setFormData] = useState<ChatbotFormData | null>(null);
	const [deploymentMessages, setDeploymentMessages] = useState<
		DeploymentMessage[]
	>([]);
	const [deploymentDone, setDeploymentDone] = useState<Boolean>(false);

	// const [currentProcess, setCurrentProcess] = useState<number>(0);
	// const [hasError, setHasError] = useState<boolean>(false);
	const [statusQueryUri, setStatusQueryUri] = useState<string | null>(null);
	const stepList = [
		'Terms & Conditions',
		'Chatbot configurations',
		'Review',
		'Deployment',
	];

	const deployApp = async () => {
		if (!formData) return;

		try {
			const deployChatbotRequest: DeployChatbotRequest = {
				chatbotFormData: formData,
			};

			// Step 1 of deplopyment: Validation
			const deploymentType = formData.deployment_type;
			let deploymentMessage = 'Validating chatbot details';

			setDeploymentMessages((prev) => [
				...prev,
				{
					message: deploymentMessage,
					status: 'pending',
				},
			]);
			await validateDeployment(deployChatbotRequest);
			setDeploymentMessages(prevMessages => {
				if (prevMessages.length === 0) return prevMessages;
				const updatedMessages = [...prevMessages];
				const lastIndex = updatedMessages.length - 1;
				updatedMessages[lastIndex] = {
				  ...updatedMessages[lastIndex],
				  status: 'success'
				};
				return updatedMessages;
			  });

			if (deploymentType === 'terraform') {
				// Step 2 of deployment: Infrastructure
				deploymentMessage = 'Initialising infrastructure';
				setDeploymentMessages((prev) => [
					...prev,
					{
						message: deploymentMessage,
						status: 'pending',
					},
				]);
				await deployInfrastructure(deployChatbotRequest);
				setDeploymentMessages(prevMessages => {
					if (prevMessages.length === 0) return prevMessages;
					const updatedMessages = [...prevMessages];
					const lastIndex = updatedMessages.length - 1;
					updatedMessages[lastIndex] = {
					  ...updatedMessages[lastIndex],
					  status: 'success'
					};
					return updatedMessages;
				  });
			}

			// Step 3 of deployment: Azure deployment
			deploymentMessage = 'Deploying to azure';
			setDeploymentMessages((prev) => [
				...prev,
				{
					message: deploymentMessage,
					status: 'pending',
				},
			]);
			const appResponse = await deployApplication(deployChatbotRequest);
			setDeploymentMessages(prevMessages => {
				if (prevMessages.length === 0) return prevMessages;
				const updatedMessages = [...prevMessages];
				const lastIndex = updatedMessages.length - 1;
				updatedMessages[lastIndex] = {
				  ...updatedMessages[lastIndex],
				  status: 'success'
				};
				return updatedMessages;
			  });

			if (!appResponse.endpoint) {
				throw new Error('Application deployment failed.');
			}
			setDeploymentDone(true);
		} catch (error) {
			// setHasError(true);
			setDeploymentMessages((prev) => {
				const newMessages = [...prev];
				newMessages[newMessages.length - 1] = {
					...newMessages[newMessages.length - 1],
					status: 'error',
					message: `Error: ${error instanceof Error ? error.message : 'An unknown error occurred'}`,
				};
				return newMessages;
			});
			setDeploymentDone(true);
		}
	};

	const handleValidationNext = async (): Promise<void> => {
		if (!formData) return;

		setCurrentStep(4);
		setDeploymentMessages([]);

		try {
			await deployApp();
		} catch (error) {
			// setHasError(true);
			setDeploymentMessages((prev) => {
				const newMessages = [...prev];
				const currentMessage = newMessages[newMessages.length - 1];
				if (currentMessage) {
					newMessages[newMessages.length - 1] = {
						...currentMessage,
						status: 'error',
						message: `Error: ${error instanceof Error ? error.message : 'An unknown error occurred'}`,
					};
				}
				return newMessages;
			});
		}
	};

	const renderDeploymentMessage = (
		message: DeploymentMessage,
		index: number,
	) => {
		return (
			<div key={index} className='space-y-2'>
				<div
					className={`flex items-center gap-3 p-4 rounded-lg border
                    ${
						message.status === 'error'
							? 'border-red-200 bg-red-50'
							: message.status === 'success'
								? 'border-green-200 bg-green-50'
								: 'border-gray-200 bg-gray-50'
					}`}
				>
					{message.status === 'pending' ? (
						<Loader2 className='h-5 w-5 animate-spin text-blue-500' />
					) : message.status === 'success' ? (
						<CheckCircle className='h-5 w-5 text-green-500' />
					) : (
						<div className='h-5 w-5 rounded-full bg-red-500' />
					)}
					<span
						className={`
                        ${
							message.status === 'error'
								? 'text-red-700'
								: message.status === 'success'
									? 'text-green-700'
									: 'text-gray-700'
						}
                    `}
					>
						{message.message}
					</span>
				</div>

				{message.subMessages && message.subMessages.length > 0 && (
					<div className='ml-6 space-y-2'>
						{message.subMessages.map((subMsg, subIndex) => (
							<div
								key={subIndex}
								className={`flex items-center gap-3 p-3 rounded-lg border
                                ${
									subMsg.status === 'error'
										? 'border-red-200 bg-red-50'
										: subMsg.status === 'success'
											? 'border-green-200 bg-green-50'
											: 'border-gray-200 bg-gray-50'
								}`}
							>
								{subMsg.status === 'pending' ? (
									<Loader2 className='h-4 w-4 animate-spin text-blue-500' />
								) : subMsg.status === 'success' ? (
									<CheckCircle className='h-4 w-4 text-green-500' />
								) : subMsg.status === 'error' ? (
									<div className='h-4 w-4 rounded-full bg-red-500' />
								) : null}
								<span className='text-sm'>
									{subMsg.message}
								</span>
							</div>
						))}
					</div>
				)}
			</div>
		);
	};
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

	const handleNewDeployment = (): void => {
		setCurrentStep(1);
		setFormData(null);
		setDeploymentMessages([]);
		setDeploymentDone(false);
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
					<div className='w-full flex flex-col justify-center items-center'>
						<div className='space-y-4 w-3/4 p-8'>
							{deploymentMessages.map((msg, index) =>
								renderDeploymentMessage(msg, index),
							)}
						</div>

						{deploymentDone === true && (
							<button
								onClick={handleNewDeployment}
								type='button'
								className='w-3/4 p-8 bg-accent text-accent-foreground py-2 rounded border border-accent-foreground'
							>
								Deploy another chatbot
							</button>
						)}
					</div>
				)}
			</div>
		</div>
	);
};

export default DeploymentPage;
