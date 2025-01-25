from azure.functions import HttpResponse
from typing import Tuple
import logging
import os
import httpx
import json

def _parse_payload(payload: dict) -> Tuple[dict, str, str, dict, str]:
    message = payload.get('message', {})
    callback_query = payload.get('callback_query', {})
    chat_id = None
    text = None
    callback_data = None

    if message:
        chat_id = message['chat']['id']
        text = message['text']
    if callback_query:
        chat_id = callback_query['message']['chat']['id']
        callback_data = callback_query['data']
    return message, chat_id, text, callback_query, callback_data


def _command_mapper(command_string: str, reverse: bool = False) -> str:
    command_map = {
            "command_callback_select" : "select"
        }
    
    reverse_command_map =  {
            "select" : "command_callback_select"
        }
    
    if not reverse:
        return command_map.get(command_string, "")
    else:
        return reverse_command_map.get(command_string, "")

async def _execute_url(method, params="", json="") -> HttpResponse:
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
            return HttpResponse(body="Successfully executed _execute_url", 
                                mimetype="text/plain",
                                status_code=200)
        except Exception as e:
            logging.error(f"Error executing _execute_url: {str(e)}")
            return HttpResponse(str(e), 
                                mimetype="text/plain",
                                status_code=500)
        

async def _query_chatbot(chatbot_endpoint: str, user_query: str) -> str:
    logging.warning("Executing _query_chatbot...")
    async with httpx.AsyncClient() as client:
        try:
            request_payload = {
                'query': user_query
                }
            logging.warning(f"{chatbot_endpoint}, {json.dumps(request_payload)}")
            response = await client.post(f'{chatbot_endpoint}', json=request_payload)
            return response.text
        except Exception as e:
            logging.error(f"Error executing _query_chatbot: {str(e)}")
            raise Exception("Error occured in query chatbot")


async def _echo_message(chat_id: str, text: str) -> HttpResponse:
    response_payload = {
        'chat_id': chat_id,
        'text': text
        }
    response = await _execute_url("sendMessage", json=response_payload)
    return response

