export interface Chatbot {
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
	_rid: string;
	_self: string;
	_etag: string;
	_attachments: string;
	_ts: number;
}