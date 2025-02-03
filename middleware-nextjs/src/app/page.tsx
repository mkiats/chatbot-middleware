import { LoginForm } from '@/components/login-form';
import Image from 'next/image';
import { redirect } from 'next/navigation';

export default function Home() {
	redirect('/dashboard');
	// return (
		// <div className='flex w-full h-3/5 justify-center items-center'>
		// 	<LoginForm/>
		// </div>
	// );
}
