'use client';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import {
	Form,
	FormControl,
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from '../ui/form';
import { Input } from '@/components/ui/input';
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useAuth } from '@/lib/contexts/AuthContext';
import { CircleCheckIcon, CircleXIcon } from 'lucide-react';
// First, let's define the ChatbotStatus enum
export const ChatbotStatusEnum = z.enum(['inactive', 'active', 'debug']);
// export const DeploymentTypeEnum = z.enum(['managed', 'custom']);
export const DeploymentTypeEnum = z.enum(['managed', 'custom', 'terraform']);

// File validation schema
const MAX_FILE_SIZE = 500 * 1024 * 1024; // 50MB
const ACCEPTED_FILE_TYPES = ['application/zip', 'application/x-zip-compressed'];

const FileSchema = z.custom<File>(
	(file) => {
		// Type guard to check if the value is a File object
		if (!(file instanceof File)) {
			return false;
		}

		// Validate size
		if (file.size > MAX_FILE_SIZE) {
			return false;
		}

		// Validate type
		if (!ACCEPTED_FILE_TYPES.includes(file.type)) {
			return false;
		}

		return true;
	},
	{
		message: 'Please provide a valid ZIP file under 50MB',
	},
);

// Base schema with common fields
const ChatbotBaseSchema = z.object({
	name: z
		.string()
		.max(40)
		.regex(/^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$/)
		.default('placeholder_name'),
	version: z.string().default('1.0.0'),
	description: z.string().max(250).default(''),
	status: ChatbotStatusEnum.default('active'),
	developer_id: z.string().optional(),
	telegram_support: z.boolean().default(true),
	created_at: z.number().int().optional(),
	updated_at: z.number().int().optional(),
	document: FileSchema,
});

const deploymentDescriptions = {
	managed: 'Recommended for projects with no specific naming requirements',
	custom: 'Use when you have already created Azure resources',
	terraform:
		'Recommended when you need to create Azure resources using Infrastructure as Code',
};

// Managed deployment type schema
const ManagedDeploymentSchema = ChatbotBaseSchema.extend({
	deployment_type: z.literal('managed'),
	resource_group_name: z.string().max(63).optional(), // Optional for managed
	location: z.string().max(63).default('southeastasia'),
	subscription_id: z.string().max(63).optional(),
	app_insights_name: z.string().max(63).optional(),
	storage_account_name: z.string().max(63).optional(),
	client_id: z.string().max(63).optional(),
	client_secret: z.string().max(63).optional(),
	tenant_id: z.string().max(63).optional(),
});

// Custom deployment type schema
const CustomDeploymentSchema = ChatbotBaseSchema.extend({
	deployment_type: z.literal('custom'),
	resource_group_name: z
		.string()
		.max(63)
		.regex(/^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$/),
	location: z.string().max(63).default('southeastasia'),
	subscription_id: z.string().max(63),
	app_insights_name: z
		.string()
		.max(63)
		.regex(/^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$/),
	storage_account_name: z
		.string()
		.max(63)
		.regex(/^[a-zA-Z0-9]+$/),
	client_id: z.string().max(63),
	client_secret: z.string().max(63),
	tenant_id: z.string().max(63),
});

// Terraform deployment type schema
const TerraformDeploymentSchema = ChatbotBaseSchema.extend({
	deployment_type: z.literal('terraform'),
	subscription_id: z.string().max(63),
	location: z.string().max(63).default('southeastasia'),
	resource_group_name: z
		.string()
		.max(63)
		.regex(/^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$/),
	app_insights_name: z
		.string()
		.max(63)
		.regex(/^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$/),
	storage_account_name: z
		.string()
		.max(63)
		.regex(/^[a-zA-Z0-9]+$/),
	client_id: z.string().max(63),
	client_secret: z.string().max(63),
	tenant_id: z.string().max(63),
});

// Combined schema using discriminated union
const ChatbotSchema = z.discriminatedUnion('deployment_type', [
	CustomDeploymentSchema,
	ManagedDeploymentSchema,
	TerraformDeploymentSchema,
]);

// Type inference
export type ChatbotFormData = z.infer<typeof ChatbotSchema>;

interface ChatbotCreationFormProps {
	onSubmit: (data: ChatbotFormData) => void;
	className?: string;
	buttonText?: string;
	title?: string;
}

export const ChatbotCreationForm: React.FC<ChatbotCreationFormProps> = ({
	onSubmit,
	className = '',
	buttonText = 'Submit',
	title = 'Chatbot details',
}) => {
	const { developerUuid } = useAuth();

	// 1. Define your form.
	const form = useForm<z.infer<typeof ChatbotSchema>>({
		resolver: zodResolver(ChatbotSchema),
		defaultValues: {
			name: 'Placeholder-Name',
			version: '1.0.0',
			description: 'Placeholder description',
			status: 'active',
			developer_id: developerUuid!,
			telegram_support: true,
			document: undefined,
			deployment_type: 'managed',
			subscription_id: undefined,
			location: 'southeastasia',
			resource_group_name: undefined,
			app_insights_name: undefined,
			storage_account_name: undefined,
			client_id: undefined,
			client_secret: undefined,
			tenant_id: undefined,
		},
	});

	const deploymentType = form.watch('deployment_type');

	// Base fields that are common to all deployment types
	const renderBaseFields = () => (
		<>
			<FormField
				control={form.control}
				name='name'
				render={({ field }) => (
					<FormItem>
						<FormLabel>Chatbot Name</FormLabel>
						<FormControl>
							<Input
								placeholder='Enter chatbot name'
								{...field}
							/>
						</FormControl>
						<FormDescription>
							This will be the name of your Chatbot. Use
							alphanumeric characters only!
						</FormDescription>
						<FormDescription>
							✅ mkiats-chatbot | mkiats-chatbot-123
						</FormDescription>
						<FormDescription>
							❌ mkiats chatbot | mkiats_chatbot |
							mkiats,./;'chatbot
						</FormDescription>
						<FormMessage />
					</FormItem>
				)}
			/>

			<FormField
				control={form.control}
				name='version'
				render={({ field }) => (
					<FormItem>
						<FormLabel>Version</FormLabel>
						<FormControl>
							<Input placeholder='1.0.0' {...field} />
						</FormControl>
						<FormDescription>
							Current semantic version of your chatbot. Use for
							version tracking of chatbot releases.
						</FormDescription>
						<FormDescription>✅ 1.0.0 | 1.10.2</FormDescription>
						<FormDescription>
							❌ 1.2.3.4 | 12a.34b.56c
						</FormDescription>
						<FormMessage />
					</FormItem>
				)}
			/>

			<FormField
				control={form.control}
				name='description'
				render={({ field }) => (
					<FormItem>
						<FormLabel>Description</FormLabel>
						<FormControl>
							<Input
								placeholder='Describe your chatbot'
								{...field}
							/>
						</FormControl>
						<FormDescription>
							Enter a short description for other developers to
							understand your chatbot functionalities.
						</FormDescription>

						<FormMessage />
					</FormItem>
				)}
			/>

			<FormField
				control={form.control}
				name='status'
				render={({ field }) => (
					<FormItem>
						<FormLabel>Status</FormLabel>
						<Select
							onValueChange={field.onChange}
							defaultValue={field.value}
						>
							<FormControl>
								<SelectTrigger>
									<SelectValue placeholder='Select status' />
								</SelectTrigger>
							</FormControl>
							<FormDescription>
								Initial status of your deployed chatbot. Set to
								inactive if you wish to deploy your chatbot
								without enabling other users to query your
								chatbot.
							</FormDescription>
							<SelectContent>
								{ChatbotStatusEnum.options.map((status) => (
									<SelectItem key={status} value={status}>
										{status}
									</SelectItem>
								))}
							</SelectContent>
						</Select>
						<FormMessage />
					</FormItem>
				)}
			/>

			<FormField
				control={form.control}
				name='developer_id'
				render={({ field }) => (
					<FormItem>
						<FormLabel>Developer Id</FormLabel>
						<FormControl>
							<Input
								placeholder='Input your developer Id'
								{...field}
								disabled
							/>
						</FormControl>
						<FormMessage />
					</FormItem>
				)}
			/>

			<FormField
				control={form.control}
				name='telegram_support'
				render={({ field }) => (
					<FormItem className='flex flex-row items-center justify-between rounded-lg border p-4'>
						<div className='space-y-0.5'>
							<FormLabel className='text-base'>
								Telegram Support
							</FormLabel>
							<FormDescription>
								Enable Telegram integration for your chatbot to
								be displayed within the Telegram chatbot
							</FormDescription>
						</div>
						<FormControl>
							<Switch
								checked={field.value}
								onCheckedChange={field.onChange}
							/>
						</FormControl>
					</FormItem>
				)}
			/>

			<FormField
				control={form.control}
				name='document'
				render={({ field: { onChange, value, ...field } }) => (
					<FormItem>
						<FormLabel>Document Upload</FormLabel>
						<FormControl>
							<div className='flex items-center gap-2'>
								<Input
									type='file'
									accept='.zip'
									onChange={(e) => {
										const file = e.target.files?.[0];
										if (file) {
											// Pass the actual File object directly
											onChange(file);
										}
									}}
									className='cursor-pointer'
								/>
							</div>
						</FormControl>
						<FormDescription>
							Upload a ZIP file (max 50MB)
						</FormDescription>
						<FormMessage />
					</FormItem>
				)}
			/>

			<FormField
				control={form.control}
				name='deployment_type'
				render={({ field }) => (
					<FormItem>
						<FormLabel>Deployment Type</FormLabel>
						<Select
							onValueChange={field.onChange}
							defaultValue={field.value}
						>
							<FormControl>
								<SelectTrigger>
									<SelectValue placeholder='Select deployment type' />
								</SelectTrigger>
							</FormControl>
							<FormDescription>
								Managed (Recommended): Use this deployment
								method if you are new to azure!
							</FormDescription>
							<FormDescription>
								Custom: Azure function deployment only
							</FormDescription>
							<FormDescription>
								Terraform : Automatic azure resource creation +
								deployment
							</FormDescription>
							<SelectContent>
								{DeploymentTypeEnum.options.map((type) => (
									<SelectItem key={type} value={type}>
										{type.charAt(0).toUpperCase() +
											type.slice(1)}
									</SelectItem>
								))}
							</SelectContent>
						</Select>
						<FormMessage />
					</FormItem>
				)}
			/>
		</>
	);

	// Additional fields for custom and terraform deployments
	const renderDeploymentFields = () => {
		const isCustom = deploymentType === 'custom';
		const isTerraform = deploymentType === 'terraform';

		if (!isCustom && !isTerraform) return null;

		return (
			<>
				<FormField
					control={form.control}
					name='subscription_id'
					render={({ field }) => (
						<FormItem>
							<FormLabel>Subscription ID</FormLabel>
							<FormControl>
								<Input
									placeholder='Enter subscription ID'
									{...field}
								/>
							</FormControl>
							<FormDescription>
								Subscription Id can be found within the
								subscriptions tab within your azure portal
							</FormDescription>

							<FormMessage />
						</FormItem>
					)}
				/>
				<FormField
					control={form.control}
					name='resource_group_name'
					render={({ field }) => (
						<FormItem>
							<FormLabel>Resource Group Name</FormLabel>
							<FormControl>
								<Input
									placeholder='Enter resource group name'
									{...field}
								/>
							</FormControl>
							<FormDescription>
								Resource group name can be found within JsonView
								within your resource group in azure portal
							</FormDescription>
							<FormDescription>
								✅ mkiats-azure-resources
							</FormDescription>
							<FormDescription>
								❌ mkiats azure resources |
								mkiats_azure_resources
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name='app_insights_name'
					render={({ field }) => (
						<FormItem>
							<FormLabel>App Insights Name</FormLabel>
							<FormControl>
								<Input
									placeholder='Enter App Insights name'
									{...field}
								/>
							</FormControl>
							<FormDescription>
								Application insights can be found within
								JsonView within your application insights
								resource in azure portal. Ensure it is created
								within the resource group!
							</FormDescription>
							<FormDescription>
								✅ mkiats-azure-resources
							</FormDescription>
							<FormDescription>
								❌ mkiats azure resources |
								mkiats_azure_resources
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name='storage_account_name'
					render={({ field }) => (
						<FormItem>
							<FormLabel>Storage Account Name</FormLabel>
							<FormControl>
								<Input
									placeholder='Enter storage account name'
									{...field}
								/>
							</FormControl>
							<FormDescription>
								Storage account can be found within JsonView
								within your storage account resource in azure
								portal. Ensure it is created within the resource
								group!
							</FormDescription>
							<FormDescription>
								✅ mkiats1azure2resources
							</FormDescription>
							<FormDescription>
								❌ mkiats azure resources |
								mkiats_azure_resources | mkiats-azure-resources
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name='client_id'
					render={({ field }) => (
						<FormItem>
							<FormLabel>Client ID</FormLabel>
							<FormControl>
								<Input
									placeholder='Enter client ID'
									{...field}
								/>
							</FormControl>
							<FormDescription>
								Client Id/AppId is generated during Service
								principal creation. Ensure service principal
								scope is set to your resource group
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name='client_secret'
					render={({ field }) => (
						<FormItem>
							<FormLabel>Client Secret</FormLabel>
							<FormControl>
								<Input
									placeholder='Enter client secret'
									{...field}
								/>
							</FormControl>
							<FormDescription>
								Client Secret/password is generated during
								Service principal creation. Do safeguard this
								from external parties.
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>

				<FormField
					control={form.control}
					name='tenant_id'
					render={({ field }) => (
						<FormItem>
							<FormLabel>Tenant ID</FormLabel>
							<FormControl>
								<Input
									placeholder='Enter tenant ID'
									{...field}
								/>
							</FormControl>
							<FormDescription>
								Tenant Id is generated during Service principal
								creation.
							</FormDescription>
							<FormMessage />
						</FormItem>
					)}
				/>
			</>
		);
	};

	return (
		<ScrollArea className='h-full pr-4'>
			<Form {...form}>
				<form
					onSubmit={form.handleSubmit(onSubmit)}
					className={`space-y-8 ${className}`}
				>
					{renderBaseFields()}
					{renderDeploymentFields()}
					<Button type='submit' className='w-full'>
						{buttonText}
					</Button>
				</form>
			</Form>
		</ScrollArea>
	);
};
