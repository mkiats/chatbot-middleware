import azure.functions as func
import logging
import os
import httpx
import json
from dotenv import load_dotenv
# from api import start_command, list_command

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
load_dotenv()


@app.route(route="processTelegramMessage")
async def processTelegramMessage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function "processTelegramMessage" processed a request.')

    payload = req.get_json()
    logging.info(f'\n Payload:\n{payload}\n')
    [message, chat_id, text, callback_query, callback_data] = destructure_json_response(payload)


    if payload:
        try:
            if text=="/start":
                await start_command(chat_id)
            elif text=="/list":
                await list_command(chat_id)
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
    


@app.route(route="processTempMessage", auth_level=func.AuthLevel.ANONYMOUS)
def processTempMessage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )








async def execute_url(method, params="", json=""):
    with httpx.Client() as client:
        URL = os.getenv("TELEGRAM_API_URL")
        TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        try:
            if params:
                logging.info(f'\nSendMessage params payload:\n {params}\n')
            if json:
                logging.info(f'\nSendMessage json payload:\n {json}\n')
            response = client.post(f'{URL}{TOKEN}/{method}', params=params, json=json)
            # logging.info(f"executing {method}: {response}")
            return response
        except:
            logging.error(f'Error in executing {method}')



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



def inline_keyboard_button(text: str, callback_data: str = None) -> object:
    json_obj = {
        'text': text,
        'callback_data': text
    }

    return json_obj

def destructure_json_response(json_request: str) -> [str]:
    message = json_request.get('message', None)
    callback_query = json_request.get('callback_query', None)
    chat_id = None
    text = None
    callback_data = None

    if message:
        chat_id = message['chat']['id']
        text = message['text']
    if callback_query:
        chat_id = callback_query['message']['chat']['id']
        callback_data = callback_query['data']

    return [message, chat_id, text, callback_query, callback_data]
