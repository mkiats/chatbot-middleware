# from azure.cosmos import CosmosClient
# from azure.cosmos import PartitionKey
from dotenv import load_dotenv
from azure.functions import FunctionApp, HttpRequest, HttpResponse, AuthLevel
from telegramClient import TelegramClient
from backendClient import BackendClient
from azureFunctionDeployerClient import AzureFunctionDeployerClient
import logging
from chatbot import main

# Instantiate function app
load_dotenv()
app = FunctionApp(http_auth_level=AuthLevel.ANONYMOUS)


# Instantiate routes
@app.route(route="telegram")
async def process_telegram_message(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function "processTelegramMessage" processed a request.')
    theClient = TelegramClient()
    return await theClient._process_message(req)


@app.route(route="temp", auth_level=AuthLevel.ANONYMOUS)
def process_temp_message(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )

@app.route(route="chatbots/search", auth_level=AuthLevel.ANONYMOUS)
async def search_chatbots(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient._get_chatbots_by_sql(req)

@app.route(route="chatbots", auth_level=AuthLevel.ANONYMOUS)
async def get_chatbots(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient._get_chatbots(req)

@app.route(route="chatbots/activate", auth_level=AuthLevel.ANONYMOUS)
async def activate_chatbot(req: HttpRequest) -> HttpResponse:
    logging.warning('activate_chatbot executed...')
    theClient = BackendClient()
    return await theClient._activate_chatbot(req)

@app.route(route="chatbots/deactivate", auth_level=AuthLevel.ANONYMOUS)
async def deactivate_chatbot(req: HttpRequest) -> HttpResponse:
    logging.warning('deactivate_chatbot executed...')
    theClient = BackendClient()
    return await theClient._deactivate_chatbot(req)

@app.route(route="chatbots/update", auth_level=AuthLevel.ANONYMOUS)
async def update_chatbot(req: HttpRequest) -> HttpResponse:
    logging.warning('update_chatbot executed...')
    theClient = BackendClient()
    return await theClient._update_chatbot(req)

@app.route(route="chatbots/deploy/validate", auth_level=AuthLevel.ANONYMOUS)
async def deploy_chatbot_validate(req: HttpRequest) -> HttpResponse:
    logging.warning('deploy_chatbot executed...')
    theClient = AzureFunctionDeployerClient()
    return await theClient.deploy_chatbot_validate

@app.route(route="chatbots/deploy/terraform", auth_level=AuthLevel.ANONYMOUS)
async def deploy_chatbot_terraform(req: HttpRequest) -> HttpResponse:
    logging.warning('deploy_chatbot executed...')
    theClient = AzureFunctionDeployerClient()
    return await theClient.deploy_chatbot_validate(req)

@app.route(route="chatbots/deploy/azure", auth_level=AuthLevel.ANONYMOUS)
async def deploy_chatbot_full(req: HttpRequest) -> HttpResponse:
    logging.warning('deploy_chatbot executed...')
    theClient = AzureFunctionDeployerClient()
    return await theClient.deploy_chatbot_full(req)
