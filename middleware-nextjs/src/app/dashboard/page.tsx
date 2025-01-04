import { getAllChatbots } from '@/lib/api';
import { columns } from './columns';
import { DataTable } from './data-table';


async function DashboardPage() {
	const data = await getAllChatbots();
	return (
		<div className='container mx-auto py-10'>
			<DataTable columns={columns} data={data} />
		</div>
	);
}

export default DashboardPage;
