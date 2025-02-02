from common import _echo_message, _parse_payload
from chatbot import main
import azure.functions as func
import logging
import json


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="telegram", auth_level=func.AuthLevel.ANONYMOUS)
async def get_telegram_response(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.warning('Processing get_telegram_response')
        response = func.HttpResponse("Placeholder", status_code=404)
        
        # Check if request has a body
        request_body = req.get_json()

        logging.warning(request_body)
        message, chat_id, text, callback_query, callback_data = _parse_payload(request_body)

        # Get query and process it
        response_body = await main(str(text))
        
        response = await _echo_message(chat_id=chat_id, text=response_body)
        return response

    except Exception as e:
        logging.error(f"Error processing message in TelegramClient: {str(e)}")
        response = await _echo_message(chat_id=chat_id, text=f"{str(e)}")
        return response