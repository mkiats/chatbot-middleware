import { LoginForm } from '@/components/login-form';
import Image from 'next/image';

export default function Home() {
	return (
		<div className='flex w-full h-3/5 justify-center items-center'>
			<LoginForm/>
		</div>
	);
}
