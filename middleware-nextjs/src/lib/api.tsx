import { ChatbotDocument, ChatbotEntry } from '@/lib/entities';

export async function getAllChatbots(): Promise<ChatbotEntry[]> {
    function mapToChatbot(theChatbot: ChatbotDocument): ChatbotEntry {
        // Validate that the status is one of the allowed values
        const validStatus = (status: string): status is ChatbotDocument['status'] => {
            return ['active', 'inactive', 'deprecated', 'debug'].includes(status);
        };
    
        if (!validStatus(theChatbot.status)) {
            throw new Error(`Invalid status: ${theChatbot.status}`);
        }
    
        return {
            uuid: theChatbot.id,
            name: theChatbot.name,
            status: theChatbot.status, // TypeScript now knows this is valid
            endpoint: theChatbot.endpoint
        };
    }

	try {
        const response = await fetch('https://mkiats-telegram.azurewebsites.net/api/chatbots');
        
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

// export async function createChatbot(): Promise<ChatbotEntry[]> {
// 	try {
//         const response = await fetch('https://mkiats-telegram.azurewebsites.net/api/chatbots/register');
        
//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }
        
//         const data: ChatbotDocument[] = await response.json();
        

//     } catch (error) {
//         console.error('Error fetching chatbots:', error);
//         throw error;
//     }
// }