import { ChatbotFormData } from "@/components/deployment/chatbotDetailsForm";
import { Chatbot } from "./models";

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

