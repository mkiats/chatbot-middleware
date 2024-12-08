export type Chatbot = {
	uuid: string;
	name: string;
	status: 'active' | 'inactive' | 'deprecated' | 'debug';
	endpoint: string;
};

export interface ChatbotResponse {
    chatbot_uuid: string;
    chatbot_name: string;
    chatbot_endpoint: string;
    chatbot_status: string;
    // Include other fields but mark them as optional since we won't use them
    _rid?: string;
    _self?: string;
    _etag?: string;
    _attachments?: string;
    _ts?: number;
}