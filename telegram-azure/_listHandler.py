from _common import _execute_url
from entities import ChatbotCallbackData, inline_keyboard_button
from azure.functions import HttpResponse
from azure.cosmos import ContainerProxy
from cosmos import query_by_sql
import logging
import json


# # For the /list command
async def command_telegram_list(chat_id: str, container: ContainerProxy) -> HttpResponse:
    logging.warning("Executing command_telegram_list...")

    # Query active chatbot in Cosmos DB
    query = "SELECT * FROM c WHERE c.status = 'active'"
    results = await query_by_sql(container=container, queryStr=query)

    chatbots = list()
    for chatbot in results:
        theChatbotCallbackDataString = ChatbotCallbackData.create_callback_str(command="command_callback_select", chatbot_id=chatbot.get("id"))
        theInlineKeyboardButton = inline_keyboard_button(text=chatbot.get("name"), callback_data=theChatbotCallbackDataString)
        theInlineKeyboardButton = theInlineKeyboardButton.to_dict()
        chatbots.append([theInlineKeyboardButton])
    text = f'The following chatbots are available'
    inline_keyboard = {
        'inline_keyboard': chatbots
    }
    
    json_payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': inline_keyboard
    }
    try:
        response = await _execute_url("sendMessage", json=json_payload)
        return HttpResponse(
                body="Successfully executed command_telegram_list...",
                mimetype="text/plain",
                status_code=200
            ) 
    except:
        return HttpResponse(
            body="Error in executing command_telegram_list", 
            mimetype="text/plain",
            status_code=500)