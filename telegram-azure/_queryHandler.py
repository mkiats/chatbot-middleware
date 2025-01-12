from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse
from _common import _query_chatbot, _echo_message
from entities import User, Chatbot
from exceptions import TelegramException, TelegramExceptionCode
from cosmos import query_by_key
import logging



async def command_telegram_query(chat_id: str, chatbot_id: str, user_query: str, chatbot_container: ContainerProxy) -> HttpResponse:
    logging.warning("Executing command_telegram_query...")
    the_chatbot = await query_by_key(container=chatbot_container, key="id", val=chatbot_id)
    if len(the_chatbot) == 0:
        raise TelegramException(message="Unable to find chatbot", method_name="command_telegram_query", error_code=TelegramExceptionCode.NOT_FOUND, field=f"Chatbot Id: {chatbot_id}, ")
    the_chatbot = Chatbot.from_dict(the_chatbot[0])

    if the_chatbot.status != 'active':
        raise TelegramException(message=f"Expected chatbot status to be active", method_name="command_telegram_query", field=f"Chatbot status: {the_chatbot.status}" )
    
    if the_chatbot.telegram_support != True:
        raise TelegramException(message=f"Expected chatbot telegram support to be True", method_name="command_telegram_query", field=f"Chatbot telegram support: {the_chatbot.telegram_support}" )

    try:
        the_chatbot_endpoint = the_chatbot.endpoint
        the_response = await _query_chatbot(chatbot_endpoint=the_chatbot_endpoint, user_query=user_query)
        the_response_body = the_response.get_body().decode('utf-8')[1:-2]
        response = await _echo_message(chat_id=chat_id, text=the_response_body)
        return response
    except Exception as e:
        raise TelegramException(message="Error in command_telegram_query", method_name="command_telegram_query")