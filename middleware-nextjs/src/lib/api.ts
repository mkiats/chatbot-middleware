import { ChatbotFormData } from '@/components/deployment/chatbotCreationForm';
import {
	ActivateChatbotByIdRequest,
	DeactivateChatbotByIdRequest,
	DeleteChatbotRequest,
	DeployChatbotRequest,
	GetChatbotByIdRequest,
	GetChatbotsByDeveloperIdRequest,
	UpdateChatbotByIdRequest,
} from './types/requests';
import {
	ActivateChatbotByIdResponse,
	DeactivateChatbotByIdResponse,
	DeleteChatbotResponse,
	DeployApplicationResponse,
	DeployInfrastructureResponse,
	GetAllChatbotsResponse,
	GetChatbotByIdResponse,
	GetChatbotsByDeveloperIdResponse,
	UpdateChatbotByIdResponse,
	ValidateDeploymentResponse,
} from './types/responses';
import { Chatbot } from './types/models';
import { request } from 'http';

const DOMAIN_URL = process.env.NEXT_PUBLIC_LOCAL_DOMAIN
// const DOMAIN_URL = process.env.NEXT_PUBLIC_AZURE_DOMAIN;

export async function getAllChatbots(): Promise<GetAllChatbotsResponse> {
	try {
		const response = await fetch(`${DOMAIN_URL}/api/chatbots`);
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
	}
}

export async function getChatbotsByDeveloperId(
	requestObject: GetChatbotsByDeveloperIdRequest,
): Promise<GetChatbotsByDeveloperIdResponse> {
	try {
		// TODO: Add developer Id Filter
		const response = await fetch(`${DOMAIN_URL}/api/chatbots`);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
	}
}

export async function getChatbotById(
	requestObject: GetChatbotByIdRequest,
): Promise<GetChatbotByIdResponse> {
	try {
		const queryParams = new URLSearchParams({
			chatbot_id: requestObject.chatbot_id,
		});

		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots?${queryParams.toString()}`,
		);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
	}
}

export async function updateChatbotById(
	requestObject: UpdateChatbotByIdRequest,
): Promise<UpdateChatbotByIdResponse> {
	try {
		const queryParams = new URLSearchParams({
			chatbot_id: requestObject.chatbot_id,
		});
		const queryBody = {
			chatbot_name: requestObject.chatbot_name,
			chatbot_desc: requestObject.chatbot_desc,
			chatbot_status: requestObject.chatbot_status,
			chatbot_version: requestObject.chatbot_version,
			chatbot_telegram_support: requestObject.chatbot_telegram_support
		};
		console.log(
			`${DOMAIN_URL}/api/chatbots/update?${queryParams.toString()}`,
		);
		console.log(JSON.stringify(queryBody))
		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots/update?${queryParams.toString()}`,
			{
				method: 'POST',
				body: JSON.stringify(queryBody),
			},
		);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
	}
}

export async function validateDeployment(
	requestObject: DeployChatbotRequest,
): Promise<ValidateDeploymentResponse> {
	try {
		const requestFormData = new FormData();
		const chatbotFormData = requestObject.chatbotFormData;

		if (chatbotFormData.document) {
			requestFormData.append('chatbot_file', chatbotFormData.document);
		}

		const { document, ...deploymentParams } = chatbotFormData;

		// Append all other fields under 'deployment_parameter'
		requestFormData.append(
			'deployment_parameter',
			JSON.stringify(deploymentParams),
		);
		const response = await fetch(`${DOMAIN_URL}/api/chatbots/deploy/validate`, {
			method: 'POST',
			body: requestFormData,
		});
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}, ${response.body}`);
		}

		const responseBody: ValidateDeploymentResponse = await response.json();
		if (!responseBody.validation) {
			throw new Error("Validation error! Invalid parameters/file structure detected!")
		}
		return responseBody;
		
	} catch (error) {
		console.error('Error validating chatbot:', error);
		const responseBody = {
			validation: false,
			message: "Validation error! Invalid parameters/file structure detected!"
		}
		return responseBody;
	}
}

export async function deployInfrastructure(
	requestObject: DeployChatbotRequest,
): Promise<DeployInfrastructureResponse> {
	try {
		const requestFormData = new FormData();
		const chatbotFormData = requestObject.chatbotFormData;

		// Append the file with the specific key 'chatbot_file'
		if (chatbotFormData.document) {
			requestFormData.append('chatbot_file', chatbotFormData.document);
		}

		// Extract file from formData
		const { document, ...deploymentParams } = chatbotFormData;

		// Append all other fields under 'deployment_parameter'
		requestFormData.append(
			'deployment_parameter',
			JSON.stringify(deploymentParams),
		);
		const response = await fetch(`${DOMAIN_URL}/api/chatbots/deploy/infrastructure`, {
			method: 'POST',
			body: requestFormData,
		});
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const responseBody: DeployInfrastructureResponse = await response.json();
		return responseBody;
	} catch (error) {
		console.error('Error deploying infrastructure:', error);
		throw error;
	}
}

export async function deployApplication(
	requestObject: DeployChatbotRequest,
): Promise<DeployApplicationResponse> {
	try {
		const requestFormData = new FormData();
		const chatbotFormData = requestObject.chatbotFormData;

		// Append the file with the specific key 'chatbot_file'
		if (chatbotFormData.document) {
			requestFormData.append('chatbot_file', chatbotFormData.document);
		}

		// Extract file from formData
		const { document, ...deploymentParams } = chatbotFormData;

		// Append all other fields under 'deployment_parameter'
		requestFormData.append(
			'deployment_parameter',
			JSON.stringify(deploymentParams),
		);
		const response = await fetch(`${DOMAIN_URL}/api/chatbots/deploy/application`, {
			method: 'POST',
			body: requestFormData,
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const responseBody: DeployApplicationResponse = await response.json();
		return responseBody;
	} catch (error) {
		console.error('Error deploying application:', error);
		const responseBody = {
			message: "Chatbot deployment to azure failed",
			endpoint: ""
		}
		return responseBody;
	}
}

export async function activateChatbotById(
	requestObject: ActivateChatbotByIdRequest,
): Promise<ActivateChatbotByIdResponse> {
	try {
		console.log('api triggered');
		const queryParams = new URLSearchParams({
			chatbot_id: requestObject.chatbot_id,
		});
		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots/activate?${queryParams.toString()}`,
		);
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
	}
}

export async function deactivateChatbotById(
	requestObject: DeactivateChatbotByIdRequest,
): Promise<DeactivateChatbotByIdResponse> {
	try {
		const queryParams = new URLSearchParams({
			chatbot_id: requestObject.chatbot_id,
		});

		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots/deactivate?${queryParams.toString()}`,
		);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
	}
}

export async function deleteChatbot(
	chatbotParameter: DeleteChatbotRequest,
): Promise<DeleteChatbotResponse> {
	return {
		message: 'Chatbot deleted',
	};
}
