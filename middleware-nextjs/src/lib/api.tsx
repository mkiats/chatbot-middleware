import { ChatbotFormData } from '@/components/deployment/chatbotDetailsForm';
import { ChatbotDocument, ChatbotEntry } from '@/lib/entities';

export async function getAllChatbots(): Promise<ChatbotEntry[]> {
	function mapToChatbot(theChatbot: ChatbotDocument): ChatbotEntry {
		// Validate that the status is one of the allowed values
		const validStatus = (
			status: string,
		): status is ChatbotDocument['status'] => {
			return ['active', 'inactive', 'deprecated', 'debug'].includes(
				status,
			);
		};

		if (!validStatus(theChatbot.status)) {
			throw new Error(`Invalid status: ${theChatbot.status}`);
		}

		return {
			uuid: theChatbot.id,
			name: theChatbot.name,
			status: theChatbot.status, // TypeScript now knows this is valid
			endpoint: theChatbot.endpoint,
		};
	}

	try {
		const response = await fetch(
			'https://mkiats-telegram.azurewebsites.net/api/chatbots',
		);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const data: ChatbotDocument[] = await response.json();

		return data.map(mapToChatbot);
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
	}
}
export interface DeploymentResponse {
    message: string;
    endpoint: string;
  }

export async function createChatbot(
	chatbotFormData: ChatbotFormData,
): Promise<string> {
	try {
		const requestFormData = new FormData();

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

		// const response = await fetch('https://mkiats-telegram.azurewebsites.net/api/chatbots/register');
		const response = await fetch(
			'http://localhost:7071/api/chatbots/deploy',
			{
				method: 'POST',
				body: requestFormData,
			},
		);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const deploymentResponse: DeploymentResponse = await response.json();
		return deploymentResponse.message;
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		throw error;
	}
}
