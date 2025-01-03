export type ChatbotEntry = {
	uuid: string;
	name: string;
	status: 'active' | 'inactive' | 'deprecated' | 'debug';
	endpoint: string;
};

export interface ChatbotBase {
    id: string;
    version: string;
    endpoint: string;
    name: string;
    description: string;
    status: 'active' | 'inactive';
    developer_id: string;
    telegram_support: boolean;
    deployment_resource: string;
    created_at: number;
    updated_at: number;
}

// Cosmos DB document type
export interface ChatbotDocument extends ChatbotBase {
    _rid: string;
    _self: string;
    _etag: string;
    _attachments: string;
    _ts: number;
}