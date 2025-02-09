from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse
from _common import _query_chatbot, _echo_message
from entities import User, Chatbot, ChatbotStatus
from exceptions import TelegramException, TelegramExceptionCode
from cosmos import query_by_key
import logging



async def command_telegram_query(chat_id: str, chatbot_id: str, user_query: str, chatbot_container: ContainerProxy, user_container: ContainerProxy) -> HttpResponse:
    try:
        logging.warning("Executing command_telegram_query...")
        query_result = await query_by_key(container=chatbot_container, key="id", val=chatbot_id)
        user_result = await query_by_key(container=user_container, key="id", val=chat_id)
        the_chatbot: Chatbot = query_result[0]
        the_user: User = user_result[0]

        # Chatbot not found
        if len(the_chatbot) == 0:
            response_msg =  f"No chatbots of that name found! Try /list to refresh the chatbot list."
        
        the_chatbot = Chatbot.from_dict(the_chatbot)
        the_user = User.from_dict(the_user)

        # Chatbot not acgtive
        if the_chatbot.status != ChatbotStatus.ACTIVE:
            response_msg = f"{the_chatbot.name}'s currently not active, Try /list to refresh the chatbot list."

        # Chatbot does not require telegram
        elif the_chatbot.telegram_support != True:
            response_msg = f"{the_chatbot.name}'s currently doesn't support telegram, Try /list to refresh the chatbot list."

        elif the_user.is_querying == True:
            response_msg = f"Please wait for the current query to finish."
        else:
            the_user.update_is_querying(True)
            user_container.upsert_item(body=the_user.to_dict())
            the_chatbot_endpoint = the_chatbot.endpoint
            logging.warning(the_chatbot_endpoint)
            response_msg = await _query_chatbot(chatbot_endpoint=the_chatbot_endpoint, user_query=user_query)
            logging.warning(response_msg)
        response = await _echo_message(chat_id=chat_id, text=response_msg)
        return response
    except Exception as e:
        response_msg = f"Unknown error occured when querying chatbot, Try /list to refresh and select another chatbot."
        response = await _echo_message(chat_id, text=response_msg)
        return response
    finally:
        the_user.update_is_querying(False)
        user_container.upsert_item(body=the_user.to_dict())