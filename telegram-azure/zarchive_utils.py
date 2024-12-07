import logging
import os
import httpx
import json

# def destructure_json_response(json_request: str) -> [str]:
#     message = json_request.get('message', None)
#     callback_query = json_request.get('callback_query', None)
#     chat_id = None
#     text = None
#     callback_data = None

#     if message:
#         chat_id = message['chat']['id']
#         text = message['text']
#     if callback_query:
#         chat_id = callback_query['message']['chat']['id']
#         callback_data = callback_query['data']

#     return [message, chat_id, text, callback_query, callback_data]

# async def execute_url(method, params="", json=""):
#     with httpx.Client() as client:
#         URL = os.getenv("TELEGRAM_API_URL")
#         TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

#         try:
#             if params:
#                 logging.info(f'\nSendMessage params payload:\n {params}\n')
#             if json:
#                 logging.info(f'\nSendMessage json payload:\n {json}\n')
#             response = client.post(f'{URL}{TOKEN}/{method}', params=params, json=json)
#             # logging.info(f"executing {method}: {response}")
#             return response
#         except:
#             logging.error(f'Error in executing {method}')

