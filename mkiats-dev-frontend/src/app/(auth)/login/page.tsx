'use client';

import { GalleryVerticalEnd } from 'lucide-react';

import { cn } from '@/lib/utils';
// import { Button } from '@/components/ui/button';
// import { Input } from '@/components/ui/input';
// import { Label } from '@/components/ui/label';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { useAuth } from '@/lib/contexts/AuthContext';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

const BACKEND_URL = process.env.NEXT_PUBLIC_AZURE_BACKEND_DOMAIN;

export default function LoginForm({
	className,
	...props
}: React.ComponentPropsWithoutRef<'div'>) {
	const router = useRouter();
	const { login } = useAuth();
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState('');

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		try {
			const response = await fetch(`${BACKEND_URL}/api/login`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password }),
			});
			const data = await response.json();
			if (response.ok) {
				console.log(data);
				const { developer_id,  name } = data;
				login(developer_id, name);
			} else {
				throw new Error('Login failed. Please try again.');
			}
		} catch (error) {
			console.error('Failed to verify:', error);
		}
	};

	return (
		<div className={`flex flex-col gap-6 ${className}`}>
			<div className='flex flex-col gap-6'>
				<form onSubmit={handleSubmit} className='p-6 md:p-8'>
					{/* Header */}
					<header className='flex flex-col items-center text-center mb-6'>
						<div className='flex h-8 w-8 items-center justify-center rounded-md'>
							<GalleryVerticalEnd className='h-6 w-6' />
						</div>
						<h1 className='text-xl font-bold'>
							Welcome to Elunify.
						</h1>
					</header>

					{/* Error Alert */}
					{error && (
						<Alert variant='destructive' className='mb-6'>
							<AlertDescription>{error}</AlertDescription>
						</Alert>
					)}

					{/* Form Fields */}
					<div className='space-y-6'>
						<div className='space-y-2'>
							<Label htmlFor='email'>Email</Label>
							<Input
								id='email'
								type='email'
								placeholder='m@example.com'
								required
								value={email}
								onChange={(e) => setEmail(e.target.value)}
								disabled={isLoading}
							/>
						</div>

						<div className='space-y-2'>
							<div className='flex items-center justify-between'>
								<Label htmlFor='password'>Password</Label>
								<a
									href='#'
									className='text-sm hover:underline underline-offset-2'
								>
									Forgot your password?
								</a>
							</div>
							<Input
								id='password'
								type='password'
								required
								value={password}
								onChange={(e) => setPassword(e.target.value)}
								disabled={isLoading}
							/>
						</div>

						<Button
							type='submit'
							className='w-full'
							disabled={isLoading}
						>
							{isLoading ? 'Logging in...' : 'Login'}
						</Button>

						<p className='text-center text-sm'>
							Don't have an account?{' '}
							<a
								href='#'
								className='underline underline-offset-4'
							>
								Sign up
							</a>
						</p>
					</div>
				</form>
			</div>

			{/* Terms and Privacy */}
			<footer className='text-center text-xs text-muted-foreground'>
				<p>
					By clicking continue, you agree to our{' '}
					<a
						href='#'
						className='underline underline-offset-4 hover:text-primary'
					>
						Terms of Service
					</a>{' '}
					and{' '}
					<a
						href='#'
						className='underline underline-offset-4 hover:text-primary'
					>
						Privacy Policy
					</a>
					.
				</p>
			</footer>
		</div>
	);
}
