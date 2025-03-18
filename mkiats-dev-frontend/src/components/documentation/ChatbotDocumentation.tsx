import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';
import { Info } from 'lucide-react';
import Image from 'next/image';

interface DocSectionProps {
	title: string;
	children: React.ReactNode;
}

interface FieldExamples {
	valid?: string;
	invalid?: string;
}

interface FieldDocProps {
	title: string;
	description: string;
	examples?: FieldExamples;
	notes?: string;
	children?: React.ReactNode;
}

const DocSection: React.FC<DocSectionProps> = ({ title, children }) => (
	<div className='mb-8'>
		<h2 className='text-2xl font-semibold mb-4 text-foreground'>{title}</h2>
		{children}
	</div>
);

const FieldDoc: React.FC<FieldDocProps> = ({
	title,
	description,
	examples = null,
	notes = null,
	children
}) => (
	<Card className='mb-4'>
		<CardHeader>
			<CardTitle className='text-lg'>{title}</CardTitle>
		</CardHeader>
		<CardContent>
			<p className='mb-2'>{description}</p>
			{examples && (
				<div className='mt-2'>
					<p className='font-medium text-foreground'>Examples:</p>
					<div className='ml-4'>
						{examples.valid && (
							<p className='text-green-600'>
								✓ Valid: {examples.valid}
							</p>
						)}
						{examples.invalid && (
							<p className='text-red-600'>
								✗ Invalid: {examples.invalid}
							</p>
						)}
					</div>
				</div>
			)}
			{notes && (
				<Alert className='mt-4'>
					<Info className='h-4 w-4' />
					<AlertTitle>Note</AlertTitle>
					<AlertDescription>{notes}</AlertDescription>
				</Alert>
			)}
		</CardContent>
		{children}
	</Card>
);

interface ChatbotFormDocumentationProps {
	className?: string;
}

const ChatbotDocumentation: React.FC<ChatbotFormDocumentationProps> = ({
	className = '',
}) => {
	return (
		<ScrollArea className={`h-full ${className}`}>
			<div className='max-w-4xl mx-auto p-6'>
				<h1 className='text-2xl font-bold mb-6'>
					Chatbot Creation Form Documentation
				</h1>

				<DocSection title='Basic Information'>
					<FieldDoc
						title='Chatbot Name'
						description='The unique identifier for your chatbot. Must contain only alphanumeric characters and hyphens.'
						examples={{
							valid: 'mkiats-chatbot, mkiats-chatbot-123',
							invalid:
								"mkiats chatbot, mkiats_chatbot, mkiats,./;'chatbot",
						}}
					/>

					<FieldDoc
						title='Version'
						description='Semantic version number for tracking chatbot releases.'
						examples={{
							valid: '1.0.0, 1.10.2',
							invalid: '1.2.3.4, 12a.34b.56c',
						}}
					/>

					<FieldDoc
						title='Description'
						description="A brief description of your chatbot's functionality, limited to 250 characters."
					/>
				</DocSection>

				<DocSection title='Code Configuration'>
					<FieldDoc
						title='Document Upload'
						description="Upload your chatbot's implementation files."
						notes='Accept ZIP files only, maximum size 50MB.'
					>	
					<div className='flex justify-center items-center rounded-md w-full h-full mb-8'>
						<Image
							src='/code-template.jpg'
							width={500}
      						height={500}
							alt="Round image"
  							className="rounded-xl"
						/>
					</div>
					</FieldDoc>
				</DocSection>

				<DocSection title='Deployment Configuration'>
					<FieldDoc
						title='Deployment Type'
						description='Choose between three deployment options:'
						notes={`
                              - Managed: Recommended for new users, automated resource management
                              - Custom: For pre-existing Azure resources
                              - Terraform: For Infrastructure as Code deployment
                              `}
					/>
				</DocSection>

				<DocSection title='Azure Configuration'>
					<FieldDoc
						title='Subscription ID'
						description='Your Azure subscription identifier.'
						notes='Found in the Subscriptions tab of the Azure portal.'
					/>

					<FieldDoc
						title='Resource Group Name'
						description='Name of the Azure resource group containing your chatbot resources.'
						examples={{
							valid: 'mkiats-azure-resources',
							invalid:
								'mkiats azure resources, mkiats_azure_resources',
						}}
					/>

					<FieldDoc
						title='Storage Account Name'
						description='Name of your Azure storage account. Must be unique across Azure.'
						examples={{
							valid: 'mkiats1azure2resources',
							invalid:
								'mkiats-azure-resources, mkiats_azure_resources',
						}}
						notes='Must be lowercase letters and numbers only, no special characters.'
					/>
				</DocSection>

				<DocSection title='Service Principal Details'>
					<FieldDoc
						title='Client ID'
						description='The Application (client) ID of your Azure service principal.'
						notes='Generated during service principal creation. Required for authentication.'
					/>

					<FieldDoc
						title='Client Secret'
						description='The secret key for your service principal.'
						notes='Treat this as sensitive information. Store securely and never share publicly.'
					/>

					<FieldDoc
						title='Tenant ID'
						description='Your Azure AD tenant ID.'
						notes='Found in Azure Active Directory properties or during service principal creation.'
					/>
				</DocSection>

				<DocSection title='Additional Settings'>
					<FieldDoc
						title='Status'
						description='Initial operational status of your chatbot.'
						notes={`
              - Active: Chatbot is fully operational
              - Inactive: Chatbot is deployed but not processing queries
              - Debug: Chatbot is in debugging mode
            `}
					/>

					<FieldDoc
						title='Telegram Support'
						description='Enable integration with Telegram platform.'
						notes='When enabled, your chatbot will be accessible through Telegram messenger.'
					/>
				</DocSection>
			</div>
		</ScrollArea>
	);
};

export default ChatbotDocumentation;
