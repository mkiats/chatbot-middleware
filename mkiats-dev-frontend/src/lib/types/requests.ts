import { ChatbotFormData } from '@/components/deployment/chatbotCreationForm';
import { Chatbot } from './models';

export interface GetChatbotsByDeveloperIdRequest {
	developer_id: string;
}

export interface GetChatbotByIdRequest {
	chatbot_id: string;
}

export interface UpdateChatbotByIdRequest {
	chatbot_id: string;
	chatbot_name: string;
	chatbot_desc: string;
	chatbot_version: string;
	chatbot_status: string;
	chatbot_telegram_support: boolean;
}

export interface DeployChatbotRequest {
	chatbotFormData: ChatbotFormData;
}

export interface ActivateChatbotByIdRequest {
	chatbot_id: string;
}

export interface DeactivateChatbotByIdRequest {
	chatbot_id: string;
}

export interface DeleteChatbotRequest {
	message: string;
	endpoint: string;
}