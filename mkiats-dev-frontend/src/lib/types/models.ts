export interface Chatbot {
	id: string;
	version: string;
	endpoint: string;
	name: string;
	description: string;
	status: 'active' | 'inactive';
	developer_id: string;
	telegram_support: boolean;
	deployment_resource: DeploymentResource;
	created_at: number;
	updated_at: number;
	_rid?: string;
	_self?: string;
	_etag?: string;
	_attachments?: string;
	_ts?: number;
}

export interface DeploymentResource {
	deployment_type: 'managed' | 'custom' | 'terraform';
	resource_group_name: string;
	location: string;
	subscription_id: string;
	app_insights_name: string;
	storage_account_name: string;
  }

export enum TerraformStatus {
	PENDING = "pending",
	CREATING_VARS = "creating_vars",
	INITIALIZING = "initializing",
	PLANNING = "planning",
	APPLYING = "applying",
	COMPLETE = "complete",
	FAILED = "failed"
}

export interface DeploymentMessage {
	message: string;
	status: 'pending' | 'success' | 'error';
	subMessages?: Array<{
		message: string;
		status: 'pending' | 'success' | 'error';
	}>;
}