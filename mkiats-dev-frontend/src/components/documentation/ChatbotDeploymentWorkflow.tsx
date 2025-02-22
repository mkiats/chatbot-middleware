import React from 'react';
import { ArrowRight, ArrowDown } from 'lucide-react';
import { ScrollArea } from '@radix-ui/react-scroll-area';

interface FlowNodeProps {
	title: string;
	description?: string;
	type?: 'start' | 'process' | 'deployment' | 'end' | 'validation';
	children?: React.ReactNode;
	className?: string;
}

const FlowNode: React.FC<FlowNodeProps> = ({
	title,
	description,
	type = 'process',
	children,
	className = '',
}) => {
	const getBgColor = () => {
		switch (type) {
			case 'start':
				return 'bg-green-100 border-green-500 dark:bg-green-900';
			case 'validation':
				return 'bg-orange-100 border-orange-500 dark:bg-orange-900';
			case 'deployment':
				return 'bg-blue-100 border-blue-500 dark:bg-blue-900';
			case 'end':
				return 'bg-green-100 border-green-500 dark:bg-green-900';
			default:
				return 'bg-background border-gray-500 dark:bg-grey-900';
		}
	};

	return (
		<div
			className={`p-4 rounded-lg border-2 text-foreground ${getBgColor()} text-center ${className}`}
		>
			<h3 className='font-bold mb-1 text-foreground'>{title}</h3>
			{description && (
				<p className='text-sm font-semibold text-foreground'>{description}</p>
			)}
			{children}
		</div>
	);
};

const ChatbotDeploymentFlow: React.FC = () => {
	return (
		<ScrollArea className={`h-full`}>
			<div className='max-w-4xl mx-auto p-6 text-foreground'>
				<h2 className='text-2xl font-bold mb-6 text-foreground'>
					Chatbot Deployment Flow
				</h2>

				<div className='flex flex-col items-center space-y-4'>
					{/* Start */}
					<FlowNode
						title='Start Deployment'
						type='start'
						description='Begin chatbot deployment process'
					/>

					<ArrowDown className='w-6 h-6 text-gray-500' />

					{/* Choose Deployment Type */}
					<FlowNode
						title='Select Deployment Type'
						className='w-4/5'
					/>

					{/* Deployment Types */}
					<div className='flex justify-between w-full max-w-4xl'>
						<div className='flex flex-col items-center'>
							<ArrowDown className='w-6 h-6 text-gray-500 mb-4' />
							<FlowNode
								title='Managed Deployment'
								description='Automated resource creation'
							>
								<ul className='text-sm text-left mt-2'>
									<li>• Auto resource naming</li>
									<li>• Preconfigured settings</li>
								</ul>
							</FlowNode>
							<ArrowDown className='w-6 h-6 text-gray-500 mt-4' />
						</div>

						<div className='flex flex-col items-center'>
							<ArrowDown className='w-6 h-6 text-gray-500 mb-4' />
							<FlowNode
								title='Custom Deployment'
								description='Use existing resources'
							>
								<ul className='text-sm text-left mt-2'>
									<li>• Custom resource names</li>
									<li>• Manual configuration</li>
								</ul>
							</FlowNode>
							<ArrowDown className='w-6 h-6 text-gray-500 mt-4' />
						</div>

						<div className='flex flex-col items-center'>
							<ArrowDown className='w-6 h-6 text-gray-500 mb-4' />
							<FlowNode
								title='Terraform Deployment'
								description='Infrastructure as Code'
							>
								<ul className='text-sm text-left mt-2'>
									<li>• Automated provisioning</li>
									<li>• Version controlled</li>
								</ul>
							</FlowNode>
							<ArrowDown className='w-6 h-6 text-gray-500 mt-4' />
						</div>
					</div>

					{/* Configuration Step */}
					<div className='mt-8 w-4/5'>
						<FlowNode
							title='Configure Settings'
							description='Set up required parameters'
							className='flex flex-col justify-center items-center'
						>
							<ul className='text-sm text-left mt-2'>
								<li>• Azure credentials</li>
								<li>• Azure Resource details</li>
								<li>• Chatbot details</li>
							</ul>
						</FlowNode>
					</div>

					<ArrowDown className='w-6 h-6 text-gray-500' />

					{/* Validation */}
					<FlowNode
						title='Validation'
                        type='validation'
						description='Verify parameters are valid, Checks for naming conventions'
						className='w-4/5'
					/>

					<ArrowDown className='w-6 h-6 text-gray-500' />

					{/* Deployment */}
					<FlowNode
						title='Validation'
                        type='validation'
						description='Verify uploaded zip folder is valid.'
						className='w-4/5 flex flex-col justify-center items-center text-foreground'
					>
                        <ul className='text-sm text-foreground text-left'>
                            <li className='text-foreground'>• Checks for existence of chatbot.py</li>
                            <li className='text-foreground'>• Checks chatbot.py for async main method</li>
                            <li className='text-foreground'>• Checks async main method for String input and String output</li>
                            <li className='text-foreground'>• Checks for existence of requirements.txt</li>
                            <li className='text-foreground'>• Checks for existence of host.json file</li>
                        </ul>
                    </FlowNode>

					<ArrowDown className='w-6 h-6 text-gray-500' />

					{/* Deployment */}
					<FlowNode
						title='Prep for deployment'
                        type='deployment'
						description='Execute pre-deployment process'
						className='w-4/5 flex flex-col justify-center items-center text-foreground'
					>
                        <ul className='text-sm text-foreground text-left'>
                            <li className='text-foreground'>• Adds essential files like host.json</li>
                            <li className='text-foreground'>• Appends essential files to the requirements.txt</li>
                            <li className='text-foreground'>• Adds funcignore files to prevent over-compiling</li>
                        </ul>
                    </FlowNode>
					
                    <ArrowDown className='w-6 h-6 text-gray-500' />

					{/* Deployment */}
					<FlowNode
						title='Deploy'
                        type='deployment'
						description='Execute deployment process'
						className='w-4/5 flex flex-col justify-center items-center text-foreground'
					>
                        <ul className='text-sm text-foreground text-left'>
                            <li className='text-foreground'>• Generates unique function app name</li>
                            <li className='text-foreground'>• Enable Oryx build for zipdeploy</li>
                            <li className='text-foreground'>• Create function app</li>
                            <li className='text-foreground'>• Deploy files to function app</li>
                        </ul>
                    </FlowNode>

					<ArrowDown className='w-6 h-6 text-gray-500' />

					{/* End */}
					<FlowNode
						title='Deployment Complete'
						type='end'
						description='Chatbot is ready to use'
						className='w-4/5'
					/>
				</div>
			</div>
		</ScrollArea>
	);
};

export default ChatbotDeploymentFlow;
