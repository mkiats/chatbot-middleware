import json
import os
import httpx
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'
app = FastAPI()
client = httpx.AsyncClient()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Define the webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    # Get the request body as JSON
    payload = await request.json()
    chat_id = payload['message']['chat']['id']
    text = payload['message']['text']

    response_payload = {
        'chat_id': chat_id,
        'text': text
        }
    await client.post(f"{TELEGRAM_API_URL}/sendMessage", json=response_payload)

    return {"status": "success", "message": "Webhook received successfully"}