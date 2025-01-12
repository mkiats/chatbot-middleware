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
	DeployChatbotResponse,
	GetAllChatbotsResponse,
	GetChatbotByIdResponse,
	GetChatbotsByDeveloperIdResponse,
	UpdateChatbotByIdResponse,
} from './types/responses';
import { Chatbot } from './types/models';
import { request } from 'http';

// const DOMAIN_URL = process.env.NEXT_PUBLIC_LOCAL_DOMAIN
const DOMAIN_URL = process.env.NEXT_PUBLIC_AZURE_DOMAIN;

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

export async function deployChatbot(
	requestObject: DeployChatbotRequest,
): Promise<DeployChatbotResponse> {
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
		console.log(DOMAIN_URL);
		const response = await fetch(`${DOMAIN_URL}/api/chatbots/deploy`, {
			method: 'POST',
			body: requestFormData,
		});
		console.log(JSON.stringify(response));

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const deploymentResponse: DeployChatbotResponse = await response.json();
		return deploymentResponse;
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
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
