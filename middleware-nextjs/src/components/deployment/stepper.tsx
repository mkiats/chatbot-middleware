interface StepperProps {
	currentStep: number;
	stepList: String[];
}

const Stepper: React.FC<StepperProps> = ({ currentStep, stepList }) => {
	return (
		<div className='w-full max-w-4xl mx-auto py-4'>
			<div className='relative flex justify-between'>
				<div className='absolute top-3 left-0 h-px bg-gray-200 w-full' />
				<div
					className='absolute top-3 left-0 h-px bg-black transition-all duration-200'
					style={{
						width: `${((currentStep - 1) / (stepList.length - 1)) * 100}%`,
					}}
				/>

				{stepList.map((step, index) => {
					const stepNumber = index + 1;
					const isCompleted = stepNumber < currentStep;
					const isActive = stepNumber === currentStep;

					return (
						<div
							key={index}
							className='flex flex-col items-center relative'
						>
							<div
								className={`
                    w-6 h-6 rounded-full border
                    ${isCompleted || isActive ? 'border-black bg-black' : 'border-gray-300 bg-white'}
                  `}
							>
								<span
									className={`
                      absolute top-8 text-xs font-normal whitespace-nowrap
                      ${isActive ? 'text-black' : 'text-gray-500'}
                    `}
								>
									{step}
								</span>
							</div>
						</div>
					);
				})}
			</div>
		</div>
	);
};

export default Stepper;
