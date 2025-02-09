import asyncio
from typing import Any, AsyncGenerator, Dict, Generator
from dotenv import load_dotenv
from telegramClient import TelegramClient
import azure.functions as func
import logging
import json

# Instantiate function app
load_dotenv()
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Regular HTTP-triggered functions
@app.route(route="telegram")
async def process_telegram_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function "processTelegramMessage" processed a request.')
    theClient = TelegramClient()
    return await theClient._process_message(req)