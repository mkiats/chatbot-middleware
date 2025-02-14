from typing import Any
from dotenv import load_dotenv
from azureFunctionDeployerClient import AzureFunctionDeployerClient
import azure.functions as func
import azure.durable_functions as df
import logging

# Instantiate function app
load_dotenv()
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="temp", auth_level=func.AuthLevel.ANONYMOUS)
def process_temp_message(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )

@app.route(route="chatbots/deploy/validate", auth_level=func.AuthLevel.ANONYMOUS)
async def deploy_chatbot_validate(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('deploy_chatbot_validate executed...')
    theClient = AzureFunctionDeployerClient()
    return await theClient.deploy_chatbot_validate(req)

@app.route(route="chatbots/deploy/application", auth_level=func.AuthLevel.ANONYMOUS)
async def deploy_chatbot_full(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('deploy_chatbot_full executed...')
    theClient = AzureFunctionDeployerClient()
    return await theClient.deploy_chatbot_full(req)

