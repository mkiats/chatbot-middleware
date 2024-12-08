from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse
from _common import _query_chatbot, _echo_message
from entities import User
from cosmos import query_by_key
import logging



async def command_telegram_query(chat_id: str, chatbot_uuid: str, user_query: str, chatbot_container: ContainerProxy) -> HttpResponse:
    logging.warning("Executing command_telegram_query...")
    the_chatbot = await query_by_key(container=chatbot_container, key=chatbot_uuid)
    the_chatbot_endpoint = the_chatbot[0].get("chatbot_endpoint")
    the_response = await _query_chatbot(chatbot_endpoint=the_chatbot_endpoint, user_query=user_query)
    the_response_body = the_response.get_body().decode('utf-8')[1:-2]
    response = await _echo_message(chat_id=chat_id, text=the_response_body)
    return response