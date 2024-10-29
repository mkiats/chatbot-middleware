import logging
import os
import httpx
import typing

async def echo_message(chat_id: str, text: str) -> None:

    response_payload = {
        'chat_id': chat_id,
        'text': text
        }
        
    logging.info(f'\nSendMessage payload:\n {response_payload}\n')
    response = await execute_url("sendMessage", json=response_payload)

async def start_command(chat_id: str) -> None:
    
    start_msg = f"Welcome to Chatbot marketplace!\nType /list to see available chatbots"
    await echo_message(chat_id, text=start_msg)
    pass

async def list_command(chat_id: str) -> None:
    logging.info("test")
    pass


async def display_commands() -> None:
    pass


async def execute_url(method, params="", json=""):
    with httpx.Client() as client:
        URL = os.getenv("TELEGRAM_API_URL")
        TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        try:
            response = client.post(f'{URL}{TOKEN}/{method}', params=params, json=json)
            # logging.info(f"executing {method}: {response}")
            return response
        except:
            print(f'Error in executing {method}')

async def inline_keyboard_button(text: str, url==None: str) -> str:
    pass