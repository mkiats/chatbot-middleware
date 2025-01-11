import { Chatbot } from "./models";



export interface GetAllChatbotsResponse {
    chatbots: Chatbot[];
}

export interface GetChatbotsByDeveloperIdResponse {
    chatbots: Chatbot[];
}

export interface GetChatbotByIdResponse {
    chatbots: Chatbot[];
}

export interface UpdateChatbotByIdResponse {
    chatbot: Chatbot;
}

export interface ActivateChatbotByIdResponse {
    chatbot: Chatbot;
}

export interface DeactivateChatbotByIdResponse {
    chatbot: Chatbot;
}

export interface DeployChatbotResponse {
    chatbot: Chatbot;
    message: string;
}

export interface DeleteChatbotResponse {
    message: string;
}
