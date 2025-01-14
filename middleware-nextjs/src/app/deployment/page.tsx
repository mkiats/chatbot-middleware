'use client';
import {
    ChatbotCreationForm,
    ChatbotFormData,
} from '@/components/deployment/chatbotCreationForm';
import ChatbotCreationFormValidation from '@/components/deployment/chatbotCreationFormValidation';
import Stepper from '@/components/deployment/stepper';
import { TermsAndConditions } from '@/components/deployment/termsAndConditions';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';
import { CheckCircle, Loader2 } from 'lucide-react';
import { 
    deployApplication, 
    deployInfrastructure, 
    validateDeployment 
} from '@/lib/api';
import { DeployChatbotRequest } from '@/lib/types/requests';
import { useState, useEffect } from 'react';
import { useInfrastructurePolling } from '@/lib/hooks/useTerraformPolling';
import { DeploymentMessage, TerraformStatus } from '@/lib/types/models';



const DeploymentPage: React.FC = () => {
    const [currentStep, setCurrentStep] = useState<number>(1);
    const [formData, setFormData] = useState<ChatbotFormData | null>(null);
    const [deploymentMessages, setDeploymentMessages] = useState<DeploymentMessage[]>([]);
    const [currentProcess, setCurrentProcess] = useState<number>(0);
    const [hasError, setHasError] = useState<boolean>(false);
    const [statusQueryUri, setStatusQueryUri] = useState<string | null>(null);
	const stepList = [
		'Terms & Conditions',
		'Chatbot configurations',
		'Review',
		'Deployment',
	];

    // Use the polling hook
    const { 
        status: terraformStatus, 
        isPolling, 
        error: pollingError, 
        output: terraformOutput,
        startPolling, 
        stopPolling 
    } = useInfrastructurePolling(statusQueryUri);

    useEffect(() => {
		if (terraformStatus && formData?.deployment_type === 'terraform') {
			updateInfrastructureStatus(terraformStatus);
			
			// Only proceed with application deployment for terraform type
			if (terraformStatus === TerraformStatus.COMPLETE) {
				deployApp();
			}
		}
	}, [terraformStatus, formData]);

    // Handle polling errors
    useEffect(() => {
        if (pollingError) {
            setHasError(true);
            setDeploymentMessages(prev => {
                const newMessages = [...prev];
                const infraIndex = newMessages.findIndex(msg => msg.message.includes('Infrastructure'));
                if (infraIndex !== -1) {
                    newMessages[infraIndex] = {
                        ...newMessages[infraIndex],
                        status: 'error',
                        message: `Infrastructure deployment failed: ${pollingError}`
                    };
                }
                return newMessages;
            });
        }
    }, [pollingError]);

	function updateInfrastructureStatus(terraformStatus: TerraformStatus) {
		setDeploymentMessages(prev => {
			const newMessages = [...prev];
			const infraIndex = newMessages.findIndex(msg => 
				msg.message.includes('Infrastructure deployment'));
			
			if (infraIndex === -1) return newMessages;
	
			switch (terraformStatus) {
				case TerraformStatus.PENDING:
					newMessages[infraIndex] = {
						...newMessages[infraIndex],
						status: 'pending',
						subMessages: [
							{ message: 'Preparing infrastructure deployment...', status: 'pending' }
						]
					};
					break;
	
				case TerraformStatus.CREATING_VARS:
					newMessages[infraIndex] = {
						...newMessages[infraIndex],
						status: 'pending',
						subMessages: [
							{ message: 'Preparation complete', status: 'success' },
							{ message: 'Creating Terraform variables...', status: 'pending' }
						]
					};
					break;
	
				case TerraformStatus.INITIALIZING:
					newMessages[infraIndex] = {
						...newMessages[infraIndex],
						status: 'pending',
						subMessages: [
							{ message: 'Preparation complete', status: 'success' },
							{ message: 'Variables created successfully', status: 'success' },
							{ message: 'Initializing Terraform...', status: 'pending' }
						]
					};
					break;
	
				case TerraformStatus.PLANNING:
					newMessages[infraIndex] = {
						...newMessages[infraIndex],
						status: 'pending',
						subMessages: [
							{ message: 'Preparation complete', status: 'success' },
							{ message: 'Variables created successfully', status: 'success' },
							{ message: 'Terraform initialized', status: 'success' },
							{ message: 'Planning infrastructure changes...', status: 'pending' }
						]
					};
					break;
	
				case TerraformStatus.APPLYING:
					newMessages[infraIndex] = {
						...newMessages[infraIndex],
						status: 'pending',
						subMessages: [
							{ message: 'Preparation complete', status: 'success' },
							{ message: 'Variables created successfully', status: 'success' },
							{ message: 'Terraform initialized', status: 'success' },
							{ message: 'Infrastructure plan generated', status: 'success' },
							{ message: 'Applying infrastructure changes...', status: 'pending' }
						]
					};
					break;
	
				case TerraformStatus.COMPLETE:
					newMessages[infraIndex] = {
						...newMessages[infraIndex],
						status: 'success',
						message: 'Infrastructure deployment successful!',
						subMessages: [
							{ message: 'Preparation complete', status: 'success' },
							{ message: 'Variables created successfully', status: 'success' },
							{ message: 'Terraform initialized', status: 'success' },
							{ message: 'Infrastructure plan generated', status: 'success' },
							{ message: 'Infrastructure changes applied successfully', status: 'success' }
						]
					};
					break;
	
				case TerraformStatus.FAILED:
					newMessages[infraIndex] = {
						...newMessages[infraIndex],
						status: 'error',
						message: 'Infrastructure deployment failed',
						subMessages: prev[infraIndex].subMessages?.map(msg => ({
							...msg,
							status: msg.status === 'pending' ? 'error' : msg.status
						})) || []
					};
					break;
	
				default:
					console.error('Unknown TerraformStatus:', terraformStatus);
					newMessages[infraIndex] = {
						...newMessages[infraIndex],
						status: 'error',
						message: 'Unknown infrastructure deployment status',
						subMessages: [
							{ message: 'Received unexpected status from Terraform', status: 'error' }
						]
					};
			}
	
			return newMessages;
		});
	}


    const deployApp = async () => {
		if (!formData) return;
	
		try {
			const deploymentType = formData.deployment_type;
			const deploymentMessage = deploymentType === 'terraform' 
				? 'Deploying application...'
				: 'Deploying application resources...';
	
			setDeploymentMessages(prev => [...prev, {
				message: deploymentMessage,
				status: 'pending'
			}]);
	
			const deployChatbotRequest: DeployChatbotRequest = {
				chatbotFormData: formData,
			};
			
			const appResponse = await deployApplication(deployChatbotRequest);
			
			if (!appResponse.endpoint) {
				throw new Error('Application deployment failed.');
			}
	
			const successMessage = deploymentType === 'terraform'
				? 'Application deployment successful!'
				: 'Application resources deployed successfully!';
	
			setDeploymentMessages(prev => {
				const newMessages = [...prev];
				newMessages[newMessages.length - 1] = {
					...newMessages[newMessages.length - 1],
					status: 'success',
					message: successMessage
				};
				return newMessages;
			});
	
		} catch (error) {
			setHasError(true);
			setDeploymentMessages(prev => {
				const newMessages = [...prev];
				newMessages[newMessages.length - 1] = {
					...newMessages[newMessages.length - 1],
					status: 'error',
					message: `Error: ${error instanceof Error ? error.message : 'An unknown error occurred'}`
				};
				return newMessages;
			});
		}
	};

	const handleValidationNext = async (): Promise<void> => {
		if (!formData) return;
	
		setCurrentStep(4);
		setDeploymentMessages([]);
		setCurrentProcess(0);
		setHasError(false);
		setStatusQueryUri(null);
	
		try {
			// Step 1: Validation for all deployment types
			setDeploymentMessages([{
				message: 'Validating deployment parameters...',
				status: 'pending'
			}]);
			
			const deployChatbotRequest: DeployChatbotRequest = {
				chatbotFormData: formData,
			};
	
			const validationResponse = await validateDeployment(deployChatbotRequest);
			console.log(JSON.stringify(validationResponse));
			if (!validationResponse.validation) {
				throw new Error('Validation failed. Please check your deployment parameters.');
			}
	
			setDeploymentMessages(prev => [{
				...prev[0],
				status: 'success',
				message: 'Validation successful!'
			}]);
	
			// Step 2: Handle different deployment paths based on deployment_type
			const deploymentType = formData.deployment_type;
	
			if (deploymentType === 'terraform') {
				// Terraform flow: validate -> infrastructure -> application
				setDeploymentMessages(prev => [...prev, {
					message: 'Infrastructure deployment in progress...',
					status: 'pending',
					subMessages: []
				}]);
				
				const infraResponse = await deployInfrastructure(deployChatbotRequest);
				
				// Start polling with the status query URI
				setStatusQueryUri(infraResponse.statusQueryGetUri);
				startPolling();
				
				// Note: Application deployment will be triggered by the useEffect hook
				// when terraform status becomes COMPLETE
			} else if (deploymentType === 'managed' || deploymentType === 'custom') {
				// Managed/Custom flow: validate -> application
				await deployApp();
			} else {
				// Type guard for unexpected deployment types
				throw new Error(`Unsupported deployment type: ${deploymentType}`);
			}
	
		} catch (error) {
			setHasError(true);
			setDeploymentMessages(prev => {
				const newMessages = [...prev];
				const currentMessage = newMessages[newMessages.length - 1];
				if (currentMessage) {
					newMessages[newMessages.length - 1] = {
						...currentMessage,
						status: 'error',
						message: `Error: ${error instanceof Error ? error.message : 'An unknown error occurred'}`
					};
				}
				return newMessages;
			});
		}
	};

    const renderDeploymentMessage = (message: DeploymentMessage, index: number) => {
        return (
            <div key={index} className="space-y-2">
                <div className={`flex items-center gap-3 p-4 rounded-lg border
                    ${message.status === 'error' ? 'border-red-200 bg-red-50' : 
                      message.status === 'success' ? 'border-green-200 bg-green-50' : 
                      'border-gray-200 bg-gray-50'}`}
                >
                    {message.status === 'pending' ? (
                        <Loader2 className="h-5 w-5 animate-spin text-blue-500" />
                    ) : message.status === 'success' ? (
                        <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                        <div className="h-5 w-5 rounded-full bg-red-500" />
                    )}
                    <span className={`
                        ${message.status === 'error' ? 'text-red-700' : 
                          message.status === 'success' ? 'text-green-700' : 
                          'text-gray-700'}
                    `}>
                        {message.message}
                    </span>
                </div>

                {message.subMessages && message.subMessages.length > 0 && (
                    <div className="ml-6 space-y-2">
                        {message.subMessages.map((subMsg, subIndex) => (
                            <div key={subIndex} 
                                className={`flex items-center gap-3 p-3 rounded-lg border
                                ${subMsg.status === 'error' ? 'border-red-200 bg-red-50' : 
                                  subMsg.status === 'success' ? 'border-green-200 bg-green-50' : 
                                  'border-gray-200 bg-gray-50'}`}
                            >
                                {subMsg.status === 'pending' ? (
                                    <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
                                ) : subMsg.status === 'success' ? (
                                    <CheckCircle className="h-4 w-4 text-green-500" />
                                ) : subMsg.status === 'error' ? (
                                    <div className="h-4 w-4 rounded-full bg-red-500" />
                                ) : null}
                                <span className="text-sm">
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
                        <div className="space-y-4 w-3/4">
                            {deploymentMessages.map((msg, index) => 
                                renderDeploymentMessage(msg, index)
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DeploymentPage;

