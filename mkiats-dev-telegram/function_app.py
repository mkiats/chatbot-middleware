from typing import Any
from dotenv import load_dotenv
from telegramClient import TelegramClient
import azure.functions as func
import logging
import os

# Instantiate function app
load_dotenv()
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def get_health_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning(os.environ["TELEGRAM_BOT_TOKEN"])
    logging.warning(os.environ["TELEGRAM_API_URL"])
    logging.warning(os.environ["COSMOS_DB_CONNECTION_STRING"])
    return func.HttpResponse(
            "Function app health status: Up and running!",
            status_code=200
    )

# Regular HTTP-triggered functions
@app.route(route="telegram")
async def process_telegram_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function "processTelegramMessage" processed a request.')
    theClient = TelegramClient()
    return await theClient._process_message(req)