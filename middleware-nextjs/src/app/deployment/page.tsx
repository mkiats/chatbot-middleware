'use client';
import {
	ChatbotDetailsForm,
	ChatbotFormData,
} from '@/components/deployment/chatbotDetailsForm';
import ChatbotDetailsValidation from '@/components/deployment/chatbotDetailsValidation';
import Stepper from '@/components/deployment/stepper';
import { TermsAndConditions } from '@/components/deployment/termsAndConditions';
import { useState } from 'react';

const DeploymentPage = () => {
	const [currentStep, setCurrentStep] = useState(1);
	const [formData, setFormData] = useState<ChatbotFormData | null>(null);
	const [progress, setProgress] = useState(0);

	const stepList = [
		'Terms & Conditions',
		'Chatbot configurations',
		'Review',
		'Deployment',
	];

	const handleAcceptTermsAndConditions = () => {
		setCurrentStep(2);
	};

	const handleFormSubmit = (data: ChatbotFormData) => {
		setFormData(data);
		setCurrentStep(3);
	};

	const handleValidationBack = () => {
		setCurrentStep(2);
	};

	const handleValidationNext = () => {
		setCurrentStep(4);
	};

	const handleConfirm = () => {
		setCurrentStep(4);
		// Simulate progress updates
		let prog = 0;
		const interval = setInterval(() => {
			prog += 20;
			setProgress(prog);
			if (prog >= 100) {
				clearInterval(interval);
				// Here you would typically redirect to the bot dashboard
			}
		}, 1000);
	};
	return (
		<>
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
						<ChatbotDetailsForm onSubmit={handleFormSubmit} />
					)}

					{currentStep === 3 && (
						<ChatbotDetailsValidation
							formData={formData!}
							onConfirm={handleValidationNext}
							onBack={handleValidationBack}
						/>
					)}

					{currentStep === 4 && (
						<div>DEPLOYMENT PAGE</div>
					)}
				</div>
			</div>
		</>
	);
};

export default DeploymentPage;
