import { ChatbotFormData } from '@/components/deployment/chatbotDetailsForm';
import { ActivateChatbotByIdRequest, DeactivateChatbotByIdRequest, DeleteChatbotRequest, DeployChatbotRequest, GetChatbotsByDeveloperIdRequest, UpdateChatbotByIdRequest } from './types/requests';
import { ActivateChatbotByIdResponse, DeactivateChatbotByIdResponse, DeleteChatbotResponse, DeployChatbotResponse, GetAllChatbotsResponse, GetChatbotByIdResponse, GetChatbotsByDeveloperIdResponse, UpdateChatbotByIdResponse } from './types/responses';
import { Chatbot } from './types/models';

// const DOMAIN_URL = process.env.NEXT_PUBLIC_LOCAL_DOMAIN
const DOMAIN_URL = process.env.NEXT_PUBLIC_AZURE_DOMAIN

export async function getAllChatbots(): Promise<GetAllChatbotsResponse> {
	try {
		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots`,
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

export async function getChatbotsByDeveloperId(
	requestObject: GetChatbotsByDeveloperIdRequest
): Promise<GetChatbotsByDeveloperIdResponse> {
	try {
		// TODO: Add developer Id Filter
		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots`,
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

export async function getChatbotById(
	requestObject: UpdateChatbotByIdRequest
): Promise<GetChatbotByIdResponse> {
	try {
		const queryParams = new URLSearchParams({
            chatbot_id: requestObject.chatbot_id
        });

		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots?${queryParams.toString()}`
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
	requestObject: UpdateChatbotByIdRequest
): Promise<UpdateChatbotByIdResponse> {
	try {
		// TODO: Change API endpoint to updateChatbotById
		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots/update`,
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
	requestObject: DeployChatbotRequest
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
		const response = await fetch(
            `${DOMAIN_URL}/api/chatbots/deploy`,
			{
				method: 'POST',
				body: requestFormData,
			},
		);
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
	requestObject: ActivateChatbotByIdRequest
): Promise<ActivateChatbotByIdResponse> {
	try {
		const queryParams = new URLSearchParams({
            chatbot_id: requestObject.chatbot_id
        });

		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots?${queryParams.toString()}`
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
	requestObject: DeactivateChatbotByIdRequest
): Promise<DeactivateChatbotByIdResponse> {
	try {
		const queryParams = new URLSearchParams({
            chatbot_id: requestObject.chatbot_id
        });

		const response = await fetch(
			`${DOMAIN_URL}/api/chatbots?${queryParams.toString()}`
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

export async function deleteChatbot(chatbotParameter:DeleteChatbotRequest): Promise<DeleteChatbotResponse> {
	return {
		message: "Chatbot deleted"
	}
}