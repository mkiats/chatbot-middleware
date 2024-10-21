import httpx
import os
from api import execute_url
from fastapi import FastAPI, Request
from dotenv import load_dotenv


import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
load_dotenv()
app = FastAPI()

# Links telegram bot to main webhook url
@app.on_event("startup")
async def startup():
    logging.info("Re-initialising webhook")
    WEBHOOK = os.getenv("WEBHOOK_URL")
    params = {
        'url': WEBHOOK
        }
    await execute_url("setWebhook", params=params)



# Main webhook url for telegram bot
@app.post("/gateway")
async def webhook(request: Request):
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_API_URL = os.getenv("TELEGRAM_API_URL")
    TELEGRAM_URL = f'{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}'

    payload = await request.json()
    chat_id = payload['message']['chat']['id']
    text = payload['message']['text']

    response_payload = {
        'chat_id': chat_id,
        'text': text
        }

    with httpx.Client() as client:
        try:
            r = await execute_url("sendMessage", json=response_payload)
            logging.info(f'SendMessage response: {r}')
        except:
            logging.info(f'Error in sending response...')


