from azure.functions import HttpResponse
from typing import Tuple
import logging
import os
import httpx
import json
import aiohttp

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
    try:
        request_payload = {
            'query': user_query
        }
        logging.warning(f"{chatbot_endpoint}, {json.dumps(request_payload)}")
        
        async with aiohttp.request('POST', chatbot_endpoint, json=request_payload) as response:
            return await response.text()
            
    except Exception as e:
        logging.error(f"Error executing _query_chatbot: {str(e)}")
        raise Exception("Error occurred in query chatbot")


async def _echo_message(chat_id: str, text: str) -> HttpResponse:
    response_payload = {
        'chat_id': chat_id,
        'text': text
        }
    response = await _execute_url("sendMessage", json=response_payload)
    return response

