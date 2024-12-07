import logging
from typing import Tuple
from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse, HttpRequest
from cosmos import CosmosDB
from _startHandler import command_telegram_start
from _listHandler import command_telegram_list
from _selectHandler import command_telegram_select
from _common import _parse_payload, _command_mapper

class TelegramClient:
    @staticmethod
    async def _process_message(req: HttpRequest) -> HttpResponse:
        try:
            payload = req.get_json()
            message, chat_id, text, callback_query, callback_data = _parse_payload(payload)
            
            db = CosmosDB()
            await db.initialize()
            
            response = HttpResponse("Placeholder", status_code=404)
            if text == "/start":
                response = await command_telegram_start(chat_id)
            elif text == "/list":
                response = await command_telegram_list(chat_id, db.chatbot_container)
            elif callback_data and TelegramClient.validate_callback(callback_data)=="command_callback_select":
                response = await command_telegram_select(chat_id, callback_data, db.user_container, db.chatbot_container)
            elif text and False:
                # Check if chatbot has already been selected, if yes, then forward query to there
                pass
            else:
                logging.warning("No functions executed in _process_message")
            return response
            
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            return HttpResponse(str(e), status_code=500)


    @staticmethod
    def validate_callback(callback_data: str) -> str:
        logging.warning("Executing validate_callback...")
        results = callback_data.split('_')
        command_str = _command_mapper(command_string=results[0], reverse=True)
        if command_str != "":
            return command_str
        else:
            return ""