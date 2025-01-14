from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse
from _common import _query_chatbot, _echo_message
from entities import User, Chatbot, ChatbotStatus
from exceptions import TelegramException, TelegramExceptionCode
from cosmos import query_by_key
import logging



async def command_telegram_query(chat_id: str, chatbot_id: str, user_query: str, chatbot_container: ContainerProxy) -> HttpResponse:
    try:
        logging.warning("Executing command_telegram_query...")
        query_result = await query_by_key(container=chatbot_container, key="id", val=chatbot_id)
        the_chatbot = query_result[0]
        if len(the_chatbot) == 0:
            response_msg =  f"No chatbots of that name found! Try /list to refresh the chatbot list."
        
        the_chatbot = Chatbot.from_dict(the_chatbot)
        if the_chatbot.status != ChatbotStatus.ACTIVE:
            response_msg = f"{the_chatbot.name}'s currently not active, Try /list to refresh the chatbot list."
        elif the_chatbot.telegram_support != True:
            response_msg = f"{the_chatbot.name}'s currently doesn't support telegram, Try /list to refresh the chatbot list."
        else:
            the_chatbot_endpoint = the_chatbot.endpoint
            the_response = await _query_chatbot(chatbot_endpoint=the_chatbot_endpoint, user_query=user_query)
            response_msg = the_response.get_body().decode('utf-8')[1:-2]
        response = await _echo_message(chat_id=chat_id, text=response_msg)
        return response
    except Exception as e:
        response_msg = f"Unknown error occured when querying chatbot, Try /list to refresh and select another chatbot."
        response = await _echo_message(chat_id, text=response_msg)
        return response