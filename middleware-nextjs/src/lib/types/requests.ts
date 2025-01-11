import { ChatbotFormData } from "@/components/deployment/chatbotDetailsForm";
import { Chatbot } from "./models";

export interface GetChatbotsByDeveloperIdRequest {
    developer_id: string;
}

export interface GetChatbotByIdRequest {
    chatbot_id: string;
}

export interface UpdateChatbotByIdRequest {
    chatbot: Chatbot;
}

export interface DeployChatbotRequest {
    chatbotFormData: ChatbotFormData;
}

export interface DeleteChatbotRequest {
	message: string;
	endpoint: string;
}


