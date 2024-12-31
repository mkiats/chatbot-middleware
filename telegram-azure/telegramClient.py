import logging
from typing import Tuple
from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse, HttpRequest
from cosmos import CosmosDB, query_by_key, query_by_sql
from _startHandler import command_telegram_start
from _listHandler import command_telegram_list
from _selectHandler import command_telegram_select
from _queryHandler import command_telegram_query
from _common import _parse_payload, _command_mapper, _echo_message
from entities import ChatbotCallbackData

class TelegramClient:
    @staticmethod
    async def _process_message(req: HttpRequest) -> HttpResponse:
        try:
            payload = req.get_json()
            message, chat_id, text, callback_query, callback_data = _parse_payload(payload)
            
            db = CosmosDB()
            await db.initialize()
            
            response = HttpResponse("Placeholder", status_code=404)
            if False or text == "/start": # TODO: Remove False condition when finish development
                logging.warning("Flushing messages...")
                response = await command_telegram_start(chat_id)

            elif text == "/list":
                response = await command_telegram_list(chat_id, db.chatbot_container)

            elif callback_data and TelegramClient.validate_callback(callback_data)=="command_callback_select":
                response = await command_telegram_select(chat_id, callback_data, db.user_container, db.chatbot_container)

            elif text:
                theSelectedChatbot = await TelegramClient.validate_chatbot_selection(user_id=chat_id, user_container=db.user_container)
                # Check if chatbot has already been selected, if yes, then forward query to there
                if theSelectedChatbot == "":
                    text = "Chatbot has yet to be selected, /list to view all available chatbot!"
                    response = await _echo_message(chat_id=chat_id, text=text)
                else:
                    response = await command_telegram_query(chat_id=chat_id, chatbot_uuid=theSelectedChatbot, user_query=text, chatbot_container=db.chatbot_container)
                
            else:
                logging.warning("Unknown command in _process_message")
                response = await _echo_message(chat_id=chat_id, text="Unknown command detected...")
            return response
            
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            return HttpResponse(str(e), status_code=500)


    @staticmethod
    def validate_callback(callback_data: str) -> str:
        logging.warning("Executing validate_callback...")
        [short_command_str, chatbot_uuid] = ChatbotCallbackData.destructure_callback_str(callback_data)
        command_str = _command_mapper(command_string=short_command_str, reverse=True)
        if command_str != "":
            return command_str
        else:
            return ""
    
    @staticmethod
    async def validate_chatbot_selection(user_id: str, user_container: ContainerProxy) -> str:
        logging.warning("Executing validate_chatbot_selection...")
        # query = f"SELECT * FROM c WHERE c.id = {str(user_id)}"
        userResult = await query_by_key(container=user_container, key=user_id)
        theSelectedChatbot = userResult[0].get("selected_chatbot_id")
        # TODO Add a check that the chatbot is currently active
        if theSelectedChatbot != "":
            return theSelectedChatbot
        else:
            return ""

        