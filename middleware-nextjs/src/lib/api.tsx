import { Chatbot, ChatbotResponse } from '@/lib/entities';

function mapToChatbot(response: ChatbotResponse): Chatbot {
    // Validate that the status is one of the allowed values
    const validStatus = (status: string): status is Chatbot['status'] => {
        return ['active', 'inactive', 'deprecated', 'debug'].includes(status);
    };

    if (!validStatus(response.chatbot_status)) {
        throw new Error(`Invalid status: ${response.chatbot_status}`);
    }

    return {
        uuid: response.chatbot_uuid,
        name: response.chatbot_name,
        status: response.chatbot_status, // TypeScript now knows this is valid
        endpoint: response.chatbot_endpoint
    };
}

export default async function getAllChatbots(): Promise<Chatbot[]> {
	try {
        const response = await fetch('https://mkiats-telegram.azurewebsites.net/api/chatbots');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data: ChatbotResponse[] = await response.json();
        
        return data.map(mapToChatbot);
    } catch (error) {
        console.error('Error fetching chatbots:', error);
        throw error;
    }
}