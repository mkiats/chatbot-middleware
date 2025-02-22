import logging
from dotenv import load_dotenv
import os
from typing import Tuple
from azure.cosmos import ContainerProxy
import azure.functions as func
from backendClient import BackendClient
from cosmos import CosmosDB, query_by_key, query_by_sql
from entities import Chatbot, ChatbotStatus
from exceptions import BackendException, BackendExceptionCode
import json
# Instantiate function app
load_dotenv()
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def get_health_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning(os.environ["COSMOS_DB_CONNECTION_STRING"])
    return func.HttpResponse(
            "Function app health status: Up and running!",
            status_code=200
    )

@app.route(route="addDummyUser", auth_level=func.AuthLevel.ANONYMOUS)
async def addDummyUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient.addDummyUser()


@app.route(route="login", auth_level=func.AuthLevel.ANONYMOUS)
async def login(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient.login(req)

@app.route(route="chatbots/search", auth_level=func.AuthLevel.ANONYMOUS)
async def search_chatbots(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient._get_chatbots_by_sql(req)

@app.route(route="chatbots", auth_level=func.AuthLevel.ANONYMOUS)
async def get_chatbots(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient._get_chatbots(req)

@app.route(route="chatbots/activate", auth_level=func.AuthLevel.ANONYMOUS)
async def activate_chatbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('activate_chatbot executed...')
    theClient = BackendClient()
    return await theClient._activate_chatbot(req)

@app.route(route="chatbots/deactivate", auth_level=func.AuthLevel.ANONYMOUS)
async def deactivate_chatbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('deactivate_chatbot executed...')
    theClient = BackendClient()
    return await theClient._deactivate_chatbot(req)

@app.route(route="chatbots/update", auth_level=func.AuthLevel.ANONYMOUS)
async def update_chatbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('update_chatbot executed...')
    theClient = BackendClient()
    return await theClient._update_chatbot(req)
