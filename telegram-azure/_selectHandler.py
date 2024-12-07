from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse
from _common import _echo_message
from entities import User
from cosmos import query_by_key
import logging



async def command_telegram_select(chat_id: str, callback_data: str, user_container: ContainerProxy, chatbot_container: ContainerProxy) -> HttpResponse:
    logging.warning("Executing command_telegram_select...")
    [short_command_str, chatbot_uuid] = callback_data.split('_')
    theUser = User(user_uuid=chat_id, selected_chatbot=chatbot_uuid, updated_at="")
    response = user_container.upsert_item(body=theUser.to_dict())
    queryResult = query_by_key(container=chatbot_container, key=chatbot_uuid)
    selected_chatbot_name = queryResult[0].get("chatbot_name")
    start_msg = f"{selected_chatbot_name} has been chosen, future messages would be forward there!"
    response = await _echo_message(chat_id, text=start_msg)
    return response