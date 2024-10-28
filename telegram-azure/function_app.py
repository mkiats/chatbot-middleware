import azure.functions as func
import logging
import os
import httpx
from dotenv import load_dotenv

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
load_dotenv()


@app.route(route="processTelegramMessage")
async def processTelegramMessage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    payload = req.get_json()
    logging.info(payload)
    chat_id = payload['message']['chat']['id']
    text = payload['message']['text']

    response_payload = {
        'chat_id': chat_id,
        'text': text
        }
    
    if text:
        try:
            response = await execute_url("sendMessage", json=response_payload)
            logging.info(f'SendMessage response: {response_payload}')
            return func.HttpResponse(
             f"This HTTP triggered function executed successfully, text is {text}", 
             status_code=200
            )
        except:
            logging.info(f'Error in sending response...')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
async def execute_url(method, params="", json=""):
    with httpx.Client() as client:
        URL = os.getenv("TELEGRAM_API_URL")
        TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        try:
            response = client.post(f'{URL}{TOKEN}/{method}', params=params, json=json)
            logging.info(f"executing {method}: {response}")
            return response
        except:
            print(f'Error in executing {method}')

@app.route(route="processTempMessage", auth_level=func.AuthLevel.ANONYMOUS)
def processTempMessage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )