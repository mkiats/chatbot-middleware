from typing import Any
from dotenv import load_dotenv
from azureFunctionDeployerClient import AzureFunctionDeployerClient
import azure.functions as func
import logging
import os

# Instantiate function app
load_dotenv()
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def get_health_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning(os.environ["CLIENT_ID"])
    logging.warning(os.environ["TENANT_ID"])
    logging.warning(os.environ["SUBSCRIPTION_ID"])
    logging.warning(os.environ["RESOURCE_GROUP_NAME"])
    logging.warning(os.environ["APP_SERVICE_PLAN_NAME"])
    logging.warning(os.environ["STORAGE_ACCOUNT_NAME"])
    logging.warning(os.environ["APP_INSIGHTS_NAME"])
    logging.warning(os.environ["LOCATION"])
    logging.warning(os.environ["COSMOS_DB_CONNECTION_STRING"])
    return func.HttpResponse(
            "Function app health status: Up and running!",
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

