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
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Chatbot } from '@/lib/types/models';

// Schema for the deployment resource
const DeploymentResourceSchema = z.object({
	deployment_type: z.enum(['managed', 'custom', 'terraform']),
	resource_group_name: z.string(),
	location: z.string(),
	subscription_id: z.string(),
	app_insights_name: z.string(),
	storage_account_name: z.string(),
});

// Schema for the view/edit form
const ChatbotViewSchema = z.object({
	id: z.string(),
	version: z.string(),
	endpoint: z.string(),
	name: z.string(),
	description: z.string(),
	status: z.enum(['active', 'inactive']),
	developer_id: z.string(),
	telegram_support: z.boolean(),
	deployment_resource: DeploymentResourceSchema,
	created_at: z.number(),
	updated_at: z.number(),
});

type ChatbotViewData = z.infer<typeof ChatbotViewSchema>;

interface ChatbotViewFormProps {
	chatbot: Chatbot;
	onSubmit: (data: Chatbot) => void;
	isEditing: boolean;
	onEditToggle: () => void;
	className?: string;
}

export const ChatbotViewForm: React.FC<ChatbotViewFormProps> = ({
	chatbot,
	onSubmit,
	isEditing,
	onEditToggle,
	className = '',
}) => {
	const form = useForm<ChatbotViewData>({
		resolver: zodResolver(ChatbotViewSchema),
		defaultValues: {
			id: chatbot.id,
			version: chatbot.version,
			endpoint: chatbot.endpoint,
			name: chatbot.name,
			description: chatbot.description,
			status: chatbot.status,
			developer_id: chatbot.developer_id,
			telegram_support: chatbot.telegram_support,
			deployment_resource: chatbot.deployment_resource,
			created_at: chatbot.created_at,
			updated_at: chatbot.updated_at,
		},
	});

	// Helper function to determine if a field is editable
	const isFieldEditable = (fieldName: keyof ChatbotViewData): boolean => {
		const editableFields = ['name', 'version', 'description', 'status', 'telegram_support'];
		return isEditing && editableFields.includes(fieldName);
	};

	// Helper function to format timestamp
	const formatTimestamp = (timestamp: number): string => {
		return new Date(timestamp * 1000).toLocaleString();
	};

	return (
		<ScrollArea className='h-full pr-4'>
			<Form {...form}>
				<form
					onSubmit={form.handleSubmit(onSubmit)}
					className={`space-y-8 ${className}`}
				>
					{/* Basic Information Section */}
					<Card>
						<CardHeader>
							<CardTitle>Basic Information</CardTitle>
						</CardHeader>
						<CardContent className='space-y-6'>
							{/* ID Field - Read Only */}

							{/* Editable Fields */}
							<FormField
								control={form.control}
								name='name'
								render={({ field }) => (
									<FormItem>
										<FormLabel>Name</FormLabel>
										<FormControl>
											<Input
												placeholder='Enter chatbot name'
												{...field}
												disabled={
													!isFieldEditable('name')
												}
											/>
										</FormControl>
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
											<Input
												{...field}
												disabled={
													!isFieldEditable('version')
												}
											/>
										</FormControl>
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
												{...field}
												disabled={
													!isFieldEditable(
														'description',
													)
												}
											/>
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>

							<FormField
								control={form.control}
								name='endpoint'
								render={({ field }) => (
									<FormItem>
										<FormLabel>Endpoint</FormLabel>
										<FormControl>
											<Input {...field} disabled />
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
											disabled={
												!isFieldEditable('status')
											}
										>
											<FormControl>
												<SelectTrigger>
													<SelectValue placeholder='Select status' />
												</SelectTrigger>
											</FormControl>
											<SelectContent>
												<SelectItem value='active'>
													Active
												</SelectItem>
												<SelectItem value='inactive'>
													Inactive
												</SelectItem>
											</SelectContent>
										</Select>
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
										</div>
										<FormControl>
											<Switch
												checked={field.value}
												onCheckedChange={field.onChange}
												disabled={
													!isFieldEditable('telegram_support')
												}
											/>
										</FormControl>
									</FormItem>
								)}
							/>
						</CardContent>
					</Card>

					{/* Deployment Configuration Section */}
					<Card>
						<CardHeader>
							<CardTitle>Deployment Configuration</CardTitle>
						</CardHeader>
						<CardContent className='space-y-6'>
							<FormField
								control={form.control}
								name='deployment_resource.deployment_type'
								render={({ field }) => (
									<FormItem>
										<FormLabel>Deployment Type</FormLabel>
										<FormControl>
											<Input {...field} disabled />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>

							<FormField
								control={form.control}
								name='deployment_resource.resource_group_name'
								render={({ field }) => (
									<FormItem>
										<FormLabel>Resource Group</FormLabel>
										<FormControl>
											<Input {...field} disabled />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>

							<FormField
								control={form.control}
								name='deployment_resource.location'
								render={({ field }) => (
									<FormItem>
										<FormLabel>Location</FormLabel>
										<FormControl>
											<Input {...field} disabled />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>

							<FormField
								control={form.control}
								name='deployment_resource.subscription_id'
								render={({ field }) => (
									<FormItem>
										<FormLabel>Subscription ID</FormLabel>
										<FormControl>
											<Input {...field} disabled />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>

							<FormField
								control={form.control}
								name='deployment_resource.app_insights_name'
								render={({ field }) => (
									<FormItem>
										<FormLabel>App Insights Name</FormLabel>
										<FormControl>
											<Input {...field} disabled />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>

							<FormField
								control={form.control}
								name='deployment_resource.storage_account_name'
								render={({ field }) => (
									<FormItem>
										<FormLabel>
											Storage Account Name
										</FormLabel>
										<FormControl>
											<Input {...field} disabled />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>
						</CardContent>
					</Card>

					{/* Additional Settings Section */}
					<Card>
						<CardHeader>
							<CardTitle>Additional Settings</CardTitle>
						</CardHeader>
						<CardContent className='space-y-6'>
							<FormField
								control={form.control}
								name='id'
								render={({ field }) => (
									<FormItem>
										<FormLabel>Chatbot ID</FormLabel>
										<FormControl>
											<Input {...field} disabled />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>

							<FormField
								control={form.control}
								name='developer_id'
								render={({ field }) => (
									<FormItem>
										<FormLabel>Developer ID</FormLabel>
										<FormControl>
											<Input {...field} disabled />
										</FormControl>
										<FormMessage />
									</FormItem>
								)}
							/>

							{/* Timestamps */}
							<div className='space-y-2 text-sm text-gray-500'>
								<div>
									Created:{' '}
									{formatTimestamp(
										form.getValues('created_at'),
									)}
								</div>
								<div>
									Updated:{' '}
									{formatTimestamp(
										form.getValues('updated_at'),
									)}
								</div>
							</div>
						</CardContent>
					</Card>

					<div className='flex justify-between gap-4'>
						<Button
							type='button'
							variant='outline'
							onClick={onEditToggle}
						>
							{isEditing ? 'Cancel' : 'Edit'}
						</Button>
						{isEditing && (
							<Button type='submit'>Save Changes</Button>
						)}
					</div>
				</form>
			</Form>
		</ScrollArea>
	);
};
