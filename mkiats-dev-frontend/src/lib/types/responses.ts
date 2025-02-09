import { Chatbot } from './models';

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

export interface ValidateDeploymentResponse {
	validation: Boolean;
    message: string;
}

export interface DeployInfrastructureResponse {
	id: string;
	statusQueryGetUri: string;
	sendEventPostUri?: string;
	terminatePostUri?: string;
	rewindPostUri?: string;
	purgeHistoryDeleteUri?: string;
	restartPostUri?: string;
	suspendPostUri?: string;
	resumePostUri?: string;
}

export interface DeployApplicationResponse {
	message: string;
    endpoint: string;
}

export interface DeleteChatbotResponse {
	message: string;
}
