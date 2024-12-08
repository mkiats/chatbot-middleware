export const payments: Chatbot[] = [
	{
		id: '728ed52f',
		name: 'chatbot v1',
		status: 'active',
		endpoint: 'localhost:8080/v1',
	},
	{
		id: '489e1d42',
		name: 'chatbot v2',
		status: 'active',
		endpoint: 'localhost:8080/v2',
	},
];

import { Chatbot, columns } from './columns';
import { DataTable } from './data-table';

async function getDummyData(): Promise<Chatbot[]> {
	// Fetch data from your API here.
	return [
		{
			id: '728ed52f',
			name: 'chatbot v1',
			status: 'active',
			endpoint: 'localhost:8080/v1',
		},
		{
			id: '489e1d42',
			name: 'chatbot v2',
			status: 'active',
			endpoint: 'localhost:8080/v2',
		},
	];
}

async function DashboardPage() {
	const data = await getDummyData();
	return (
		<div className='container mx-auto py-10'>
			<DataTable columns={columns} data={data} />
		</div>
	);
}

export default DashboardPage;
