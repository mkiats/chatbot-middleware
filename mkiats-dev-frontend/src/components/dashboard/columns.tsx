'use client';

import { ColumnDef } from '@tanstack/react-table';
import { MoreHorizontal, ArrowUpDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuLabel,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Chatbot } from '@/lib/types/models';
import { ActivateChatbotByIdRequest, DeactivateChatbotByIdRequest } from '@/lib/types/requests';
import { activateChatbotById, deactivateChatbotById } from '@/lib/api';
import { useRouter } from 'next/navigation';

export const columns: ColumnDef<Chatbot>[] = [
	{
		id: 'select',
		header: ({ table }) => (
			<Checkbox
				checked={
					table.getIsAllPageRowsSelected() ||
					(table.getIsSomePageRowsSelected() && 'indeterminate')
				}
				onCheckedChange={(value) =>
					table.toggleAllPageRowsSelected(!!value)
				}
				aria-label='Select all'
			/>
		),
		cell: ({ row }) => (
			<Checkbox
				checked={row.getIsSelected()}
				onCheckedChange={(value) => row.toggleSelected(!!value)}
				aria-label='Select row'
			/>
		),
		enableSorting: false,
		enableHiding: false,
	},
	{
		accessorKey: 'name',
		header: ({ column }) => {
			return (
				<Button
					variant='ghost'
					onClick={() =>
						column.toggleSorting(column.getIsSorted() === 'asc')
					}
					className='text-left'
				>
					Name
					<ArrowUpDown className='ml-2 h-4 w-4' />
				</Button>
			);
		},
	},
	{
		accessorKey: 'status',
		header: ({ column }) => {
			return (
				<Button
					variant='ghost'
					onClick={() =>
						column.toggleSorting(column.getIsSorted() === 'asc')
					}
					className='text-left'
				>
					Status
					<ArrowUpDown className='ml-2 h-4 w-4' />
				</Button>
			);
		},
	},
	{
		accessorKey: 'telegram_support',
		header: ({ column }) => {
			return (
				<Button
					variant='ghost'
					onClick={() =>
						column.toggleSorting(column.getIsSorted() === 'asc')
					}
					className='text-left'
				>
					Telegram support
					<ArrowUpDown className='ml-2 h-4 w-4' />
				</Button>
			);
		},
	},
	{
		accessorKey: 'endpoint',
		header: ({ column }) => {
			return (
				<Button
					variant='ghost'
					onClick={() =>
						column.toggleSorting(column.getIsSorted() === 'asc')
					}
					className='text-left'
				>
					Endpoint
					<ArrowUpDown className='ml-2 h-4 w-4' />
				</Button>
			);
		},
	},
	{
		id: 'actions',
		cell: ({ row }) => {
			const chatbot = row.original;
			const router = useRouter();

            const handleActivate = async (e: React.MouseEvent<HTMLDivElement>) => {
                e.preventDefault();
                const activateChatbotRequest: ActivateChatbotByIdRequest = {
					chatbot_id: chatbot.id  // Accessing the id from the row data
                };
                const response = await activateChatbotById(activateChatbotRequest);
                window.location.reload();
            };

            const handleDeactivate = async (e: React.MouseEvent<HTMLDivElement>) => {
                e.preventDefault();
                const deactivateChatbotRequest: DeactivateChatbotByIdRequest = {
                    chatbot_id: chatbot.id  // Accessing the id from the row data
                };
                const response = await deactivateChatbotById(deactivateChatbotRequest);
                window.location.reload();
            };

			return (
				<DropdownMenu>
					<DropdownMenuTrigger asChild>
						<Button variant='ghost' className='h-8 w-8 p-0'>
							<span className='sr-only'>Open menu</span>
							<MoreHorizontal className='h-4 w-4' />
						</Button>
					</DropdownMenuTrigger>
					<DropdownMenuContent align='end'>
						<DropdownMenuLabel>Actions</DropdownMenuLabel>
						<DropdownMenuItem
							onClick={() =>
								navigator.clipboard.writeText(chatbot.endpoint)
							}
						>
							Copy chatbot endpoint
						</DropdownMenuItem>
						<DropdownMenuSeparator />
						<DropdownMenuItem className='text-primary' onClick={() => {router.push(`/dashboard/${chatbot.id}`)}} >View chatbot details</DropdownMenuItem>
						<DropdownMenuItem onClick={handleActivate} >Set active</DropdownMenuItem>
						<DropdownMenuItem onClick={handleDeactivate}>Set inactive</DropdownMenuItem>
						<DropdownMenuItem>Terminate instance</DropdownMenuItem>
					</DropdownMenuContent>
				</DropdownMenu>
			);
		},
	},
];
