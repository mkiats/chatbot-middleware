import { getAllChatbots } from '@/lib/api';
import { columns } from '../../components/dashboard/columns';
import { DataTable } from '../../components/dashboard/data-table';


async function DashboardPage() {
	const chatbotResponse = await getAllChatbots();
	const chatbots = chatbotResponse.chatbots;
	return (
		<div className='container mx-auto py-10'>
			<DataTable columns={columns} data={chatbots} />
		</div>
	);
}

export default DashboardPage;
