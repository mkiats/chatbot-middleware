from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse
from _common import _echo_message
from entities import ChatbotStatus, User, Chatbot
from exceptions import TelegramException, TelegramExceptionCode
from cosmos import query_by_key
import logging



async def command_telegram_select(chat_id: str, callback_data: str, user_container: ContainerProxy, chatbot_container: ContainerProxy) -> HttpResponse:
    try:
        logging.warning("Executing command_telegram_select...")
        [short_command_str, chatbot_id] = callback_data.split('_')
        query_result = await query_by_key(container=chatbot_container, key="id", val=chatbot_id)
        the_chatbot = query_result[0]
        if len(the_chatbot) == 0:
            response_msg =  f"No chatbots of that name found! Try /list to refresh the chatbot list."
        
        the_chatbot = Chatbot.from_dict(the_chatbot)

        # Chatbot not active
        if the_chatbot.status != ChatbotStatus.ACTIVE:
            response_msg = f"{the_chatbot.name}'s currently not active, Try /list to refresh the chatbot list."

        # Chatbot does not require telegram    
        elif the_chatbot.telegram_support != True:
            response_msg = f"{the_chatbot.name}'s currently doesn't support telegram, Try /list to refresh the chatbot list."

        else:
            the_user = User(id=chat_id, selected_chatbot_id=chatbot_id)
            user_container.upsert_item(body=the_user.to_dict())
            response_msg = f"{the_chatbot.name} has been chosen, future messages would be forward there!"
        response = await _echo_message(chat_id, text=response_msg)
        return response
    except:
        response_msg = f"Unknown error occured when selecting chatbot, Try /list to refresh and select another chatbot."
        response = await _echo_message(chat_id, text=response_msg)
        return response