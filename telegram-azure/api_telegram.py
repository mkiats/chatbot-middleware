from entities import inline_keyboard_button, ChatbotCallbackData
from utils import destructure_json_response, execute_url
from azure.cosmos import ContainerProxy
import azure.functions as func
import logging
import os
import httpx
import json

async def command_telegram_gateway(req: func.HttpRequest, user_container: ContainerProxy, chatbot_container: ContainerProxy) -> func.HttpResponse:
    payload = req.get_json()
    logging.info(f'\n Payload:\n{payload}\n')
    [message, chat_id, text, callback_query, callback_data] = destructure_json_response(payload)


    if payload:
        try:
            if text=="/start":
                await start_command(chat_id)
            elif text=="/list":
                await list_command(chat_id=chat_id, chatbot_container=chatbot_container)
            else:
                await echo_message(chat_id, callback_data)
                logging.info(f'Unknown command detected...')
            
            return func.HttpResponse(
            f"This HTTP triggered function executed successfully, text is {text}", 
            status_code=200
            )
        except:
            logging.info(f'Error in sending response...')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )








# For the /list command
async def command_telegram_list(chat_id: str, container: ContainerProxy) -> func.HttpResponse:

    # Query active chatbot in Cosmos DB
    query = "SELECT * FROM c WHERE c.status = 'active'"
    results = container.query_items(query=query, enable_cross_partition_query=True)

    chatbots = list()
    for chatbot in results:
        theChatbotCallbackData = ChatbotCallbackData(command="command_callback_selectChatbot", chatbot_uuid=chatbot.chatbot_uuid)
        chatbots.append(list(inline_keyboard_button(text=chatbot.name, callback_data=theChatbotCallbackData)))
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
        response = await execute_url("sendMessage", json=json_payload)
        return func.HttpResponse(
                "Successfully executed command_telegram_list...",
                status_code=200
            ) 
    except:
        # TODO: Create custom error exception class
        return ValueError("Error in executing command_telegram_list")

    

async def list_command(chat_id: str, chatbot_container: ContainerProxy) -> None:
    
    text_msg = f'The following chatbots are available'
    chatbot1 = {
        'text': 'CS chatbot',
        'callback_data': 'CS chatbot'
    }
    chatbot2 = {
        'text': 'HR chatbot',
        'callback_data': 'HR chatbot'
    }
    chatbot3 = {
        'text': 'Post-sales chatbot',
        'callback_data': 'Post-sales chatbot'
    }
    inline_keyboard = {
        'inline_keyboard': 
            [[chatbot1],
            [chatbot2],
            [chatbot3]]
        }
    response_payload = {
        'chat_id': chat_id,
        'text': text_msg,
        'reply_markup': inline_keyboard
        }
    response = await execute_url("sendMessage", json=response_payload)
    pass






async def echo_message(chat_id: str, text: str) -> None:

    response_payload = {
        'chat_id': chat_id,
        'text': text
        }
    response = await execute_url("sendMessage", json=response_payload)

async def start_command(chat_id: str) -> None:
    
    start_msg = f"Welcome to Chatbot marketplace!\nType /list to see available chatbots"
    await echo_message(chat_id, text=start_msg)
    pass

async def list_command(chat_id: str) -> None:
    
    text_msg = f'The following chatbots are available'
    chatbot1 = inline_keyboard_button("CS chatbot")
    chatbot2 = inline_keyboard_button("HR chatbot")
    chatbot3 = inline_keyboard_button("Post-sales chatbot")
    inline_keyboard = {
        'inline_keyboard': 
            [[chatbot1],
            [chatbot2],
            [chatbot3]]
        }
    response_payload = {
        'chat_id': chat_id,
        'text': text_msg,
        'reply_markup': inline_keyboard
        }
    response = await execute_url("sendMessage", json=response_payload)

    pass