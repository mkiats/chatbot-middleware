'use client';
import {
	ChatbotDetailsForm,
	ChatbotFormData,
} from '@/components/deployment/chatbotDetailsForm';
import ChatbotDetailsValidation from '@/components/deployment/chatbotDetailsValidation';
import Stepper from '@/components/deployment/stepper';
import { TermsAndConditions } from '@/components/deployment/termsAndConditions';
import { Progress } from '@/components/ui/progress';
import { createChatbot } from '@/lib/api';
import { ChatbotDocument } from '@/lib/entities';
import { time } from 'console';
import { useState } from 'react';

const DeploymentPage = () => {
	const [currentStep, setCurrentStep] = useState(1);
	const [formData, setFormData] = useState<ChatbotFormData | null>(null);
	const [deploymentMessage, setDeploymentMessage] = useState<String | null>(null);

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

	const handleValidationNext = async () => {
          setCurrentStep(4);
          if (formData) {
               let theDeploymentMessage = await createChatbot(formData)
               setDeploymentMessage(theDeploymentMessage)
          }
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

					{currentStep === 3 && formData && (
						<ChatbotDetailsValidation
							formData={formData}
							onConfirm={handleValidationNext}
							onBack={handleValidationBack}
						/>
					)}
					{currentStep === 4 && (
                              
                              <div className="w-full">
                              {deploymentMessage ? (
                                <p className="text-sm text-gray-600">
                                  {deploymentMessage}
                                </p>
                              ) : (
                                <Progress 
                                  value={Date.now() % 100} 
                                  className="w-full"
                                />
                              )}
                            </div>
                                   
					)}
				</div>
			</div>
		</>
	);
};

export default DeploymentPage;
