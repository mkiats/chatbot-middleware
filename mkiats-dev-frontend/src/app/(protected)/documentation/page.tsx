import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';
import { Info } from 'lucide-react';
import ChatbotDocumentation from '@/components/documentation/ChatbotDocumentation';
import ChatbotDeploymentFlow from '@/components/documentation/ChatbotDeploymentWorkflow';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface ChatbotFormDocumentationProps {
	className?: string;
}

const DocumentationPage: React.FC<ChatbotFormDocumentationProps> = ({
	className = '',
}) => {
	return (
		<div className='flex w-full'>
			<Tabs defaultValue='documentation' className='w-full flex flex-col mt-4 justify-center items-center'>
				<TabsList className='w-1/4 h-12'>
					<TabsTrigger value='documentation' className='h-5/6'>Documentation</TabsTrigger>
					<TabsTrigger value='deploymentWorkflow' className='h-5/6'>Deployment Workflow</TabsTrigger>
				</TabsList>
				<TabsContent value='documentation' className='w-full pt-12'>
					<ChatbotDocumentation />
				</TabsContent>
				<TabsContent value='deploymentWorkflow' className='w-full pt-12'>
					<ChatbotDeploymentFlow />
				</TabsContent>
			</Tabs>
		</div>
	);
};

export default DocumentationPage;
