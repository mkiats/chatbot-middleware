import { ChatbotFormData } from '@/components/deployment/chatbotCreationForm';
import {
	ActivateChatbotByIdRequest,
	DeactivateChatbotByIdRequest,
	DeleteChatbotRequest,
	DeployChatbotRequest,
	GetChatbotByIdRequest,
	GetChatbotsByDeveloperIdRequest,
	UpdateChatbotByIdRequest,
} from '@/lib/types/requests';
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
} from '@/lib/types/responses';
import { Chatbot } from '@/lib/types/models';
import { request } from 'http';

// const DOMAIN_URL = process.env.NEXT_PUBLIC_LOCAL_DOMAIN
// const DOMAIN_URL = process.env.NEXT_PUBLIC_AZURE_DOMAIN;


const BACKEND_URL = process.env.NEXT_PUBLIC_AZURE_BACKEND_DOMAIN;
// const BACKEND_URL = "http://localhost:7071";
const DEPLOYMENT_URL = process.env.NEXT_PUBLIC_AZURE_DEPLOYMENT_DOMAIN;
const TELEGRAM_URL = process.env.NEXT_PUBLIC_AZURE_TELEGRAM_DOMAIN;
const TERRAFORM_URL = process.env.NEXT_PUBLIC_AZURE_TERRAFORM_DOMAIN;

export async function getAllChatbots(): Promise<GetAllChatbotsResponse> {
	try {
		console.log(`${BACKEND_URL}/api/chatbots`)
		const response = await fetch(`${BACKEND_URL}/api/chatbots`);
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		return {
			'chatbots': []
		};
	}
}

export async function getChatbotsByDeveloperId(
	requestObject: GetChatbotsByDeveloperIdRequest,
): Promise<GetChatbotsByDeveloperIdResponse> {
	try {
		const queryParams = new URLSearchParams({
			developer_id: requestObject.developer_id,
		});
		const response = await fetch(
			`${BACKEND_URL}/api/chatbots?${queryParams.toString()}`,
		);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		return {
			'chatbots': []
		};
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
			`${BACKEND_URL}/api/chatbots?${queryParams.toString()}`,
		);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		return response.json();
	} catch (error) {
		console.error('Error fetching chatbots:', error);
		return {
			'chatbots': []
		};
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
			`${BACKEND_URL}/api/chatbots/update?${queryParams.toString()}`,
		);
		console.log(JSON.stringify(queryBody))
		const response = await fetch(
			`${BACKEND_URL}/api/chatbots/update?${queryParams.toString()}`,
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
		console.log(DEPLOYMENT_URL);

		// Append all other fields under 'deployment_parameter'
		requestFormData.append(
			'deployment_parameter',
			JSON.stringify(deploymentParams),
		);
		let newUrl = "https://mkiats-dev-deployment.azurewebsites.net/api/chatbots/deploy/validate"
		const response = await fetch(`${newUrl}`, {
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
		const chatbotFormData = requestObject.chatbotFormData;
		const { document, ...deploymentParams } = chatbotFormData;

		console.log(`${TERRAFORM_URL}/api/chatbots/deploy/infrastructure`)
		let newUrl: string = "https://mkiats-dev-terraform.victoriousriver-374dbb10.southeastasia.azurecontainerapps.io/deploy/infrastructure"
		// let newUrl: string = "http://0.0.0.0:8000/deploy/infrastructure"
		// const response = await fetch(`${DOMAIN_URL}/api/chatbots/deploy/infrastructure`, {
		console.log(JSON.stringify(deploymentParams));
		const response = await fetch(`${newUrl}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'  // This header is important
			},
			body: JSON.stringify(deploymentParams),
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
		let newUrl = `${DEPLOYMENT_URL}/api/chatbots/deploy/application`
		const response = await fetch(`${newUrl}`, {
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
			`${BACKEND_URL}/api/chatbots/activate?${queryParams.toString()}`,
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
			`${BACKEND_URL}/api/chatbots/deactivate?${queryParams.toString()}`,
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
