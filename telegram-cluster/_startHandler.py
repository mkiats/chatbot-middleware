from _common import _echo_message
from azure.functions import HttpResponse
import logging

async def command_telegram_start(chat_id: str) -> HttpResponse:
    logging.warning("Executing command_telegram_start...")
    start_msg = f"Welcome to Chatbot marketplace!\nType /list to see available chatbots"
    response = await _echo_message(chat_id, text=start_msg)
    return response