'use client';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Button } from '../ui/button';
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

// First, let's define the ChatbotStatus enum
export const ChatbotStatusEnum = z.enum(['inactive', 'active', 'debug']);
export const DeploymentTypeEnum = z.enum(['managed', 'custom', 'terraform']);

// File validation schema
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
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
	name: z.string().default('placeholder_name'),
	version: z.string().default('1.0.0'),
	description: z.string().default(''),
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
	resource_group_name: z.string().optional(), // Optional for managed
	location: z.string().default('southeastasia'),
	subscription_id: z.string().optional(),
	app_insights_name: z.string().optional(),
	storage_account_name: z.string().optional(),
	client_id: z.string().optional(),
	client_secret: z.string().optional(),
	tenant_id: z.string().optional(),
});

// Custom deployment type schema
const CustomDeploymentSchema = ChatbotBaseSchema.extend({
	deployment_type: z.literal('custom'),
	resource_group_name: z.string(),
	location: z.string().default('southeastasia'),
	subscription_id: z.string(),
	app_insights_name: z.string(),
	storage_account_name: z.string(),
	client_id: z.string(),
	client_secret: z.string(),
	tenant_id: z.string(),
});

// Terraform deployment type schema
const TerraformDeploymentSchema = ChatbotBaseSchema.extend({
	deployment_type: z.literal('terraform'),
	subscription_id: z.string().optional(),
	location: z.string().default('southeastasia'),
	resource_group_name: z.string().optional(),
	app_insights_name: z.string().optional(),
	storage_account_name: z.string().optional(),
	client_id: z.string(),
	client_secret: z.string(),
	tenant_id: z.string(),
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
	// The callback function when terms are accepted
	onSubmit: (data: ChatbotFormData) => void;
	// Optional props for customization
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
	// 1. Define your form.
	const form = useForm<z.infer<typeof ChatbotSchema>>({
		resolver: zodResolver(ChatbotSchema),
		defaultValues: {
			name: 'Placeholder-Name',
			version: '1.0.0',
			description: 'Placeholder description',
			status: 'active',
			developer_id: '257750825',
			telegram_support: true,
			document: undefined,
			deployment_type: 'managed', // Default to managed type
			subscription_id: process.env.NEXT_PUBLIC_subscription_id,
			location: 'southeastasia',
			resource_group_name: 'terraform-chatbot-deployment',
			app_insights_name: 'terraform-chatbot-deployment',
			storage_account_name: 'terraform4chatbot',
			client_id: process.env.NEXT_PUBLIC_client_id,
			client_secret: process.env.NEXT_PUBLIC_client_secret,
			tenant_id: process.env.NEXT_PUBLIC_tenant_id,
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
							Choose a unique name for your chatbot, Only use
							AlphaNumeric characters and '-' for spaces!
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
							Semantic version of your chatbot
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
								Enable Telegram integration for your chatbot
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
								managed: Recommended for projects with no
								specific naming requirements
							</FormDescription>
							<FormDescription>
								custom: Use when you have already created Azure
								resources,
							</FormDescription>
							<FormDescription>
								terraform: Recommended when you need to create
								Azure resources using Infrastructure as Code,
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
