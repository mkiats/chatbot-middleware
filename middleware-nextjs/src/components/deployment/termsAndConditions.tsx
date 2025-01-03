import React from 'react';
import { ScrollArea } from '../ui/scroll-area';

interface TermsAndConditionsProps {
	// The callback function when terms are accepted
	onAccept: () => void;
	// Optional props for customization
	className?: string;
	buttonText?: string;
	title?: string;
}

export const TermsAndConditions: React.FC<TermsAndConditionsProps> = ({
	onAccept,
	className = '',
	buttonText = 'I Accept the Terms and Conditions',
	title = 'Terms and Conditions',
}) => {
	// Handler with type safety
	const handleAccept = React.useCallback(
		(event: React.MouseEvent<HTMLButtonElement>) => {
			event.preventDefault();
			onAccept();
		},
		[onAccept],
	);

	return (
		<ScrollArea className='h-full pr-4'>
			<div className={`space-y-6 max-w-2xl mx-auto ${className}`.trim()}>
				<div className='bg-gray-50 p-6 rounded-lg space-y-4'>
					<h2 className='text-xl font-semibold'>{title}</h2>
					<div className='prose prose-sm'>
						<p>Please read and accept the following terms:</p>
						<ol className='list-decimal list-inside space-y-2'>
							<li>
								Your chatbot must comply with our content
								guidelines
							</li>
							<li>
								You are responsible for the data processed by
								your chatbot
							</li>
							<li>
								Service availability is subject to our fair
								usage policy
							</li>
							<li>
								You agree to our privacy policy and data
								handling practices
							</li>
						</ol>
					</div>
				</div>
				<button
					onClick={handleAccept}
					type='button'
					className='w-full bg-black text-white py-2 rounded hover:bg-gray-800'
				>
					{buttonText}
				</button>
			</div>
		</ScrollArea>
	);
};
