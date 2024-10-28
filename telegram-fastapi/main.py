import httpx
import os
from fastapi import FastAPI, Request
from api import execute_url


import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
from dotenv import load_dotenv
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

    payload = await request.json()
    logging.info(payload)
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


