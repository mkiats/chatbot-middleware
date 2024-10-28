import os
import httpx
import logging

async def execute_url(method, params="", json=""):
    with httpx.Client() as client:
        URL = os.getenv("TELEGRAM_API_URL")
        TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        try:
            response = client.post(f'{URL}{TOKEN}/{method}', params=params, json=json)
            logging.info(f"executing {method}: {r}")
            return response
        except:
            print(f'Error in executing {method}')