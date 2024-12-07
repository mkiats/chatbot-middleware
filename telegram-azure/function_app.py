from azure.cosmos import CosmosClient, PartitionKey
from api_telegram import command_telegram_gateway
from dotenv import load_dotenv
import azure.functions as func
import logging
import os

# Instantiate function app
load_dotenv()
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
# Instantiate cosmos db
client = CosmosClient.from_connection_string(os.getenv("COSMOS_DB_CONNECTION_STRING"))
user_database = client.create_database_if_not_exists("UserDB")
user_container = user_database.create_container_if_not_exists(id="users", partition_key=PartitionKey(path="/user_uuid"))
chatbot_database = client.create_database_if_not_exists("ChatbotDB")
chatbot_container = chatbot_database.create_container_if_not_exists(id="chatbots", partition_key=PartitionKey(path="/chatbot_uuid"))


# Instantiate routes
@app.route(route="processTelegramMessage")
async def processTelegramMessage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function "processTelegramMessage" processed a request.')
    return await command_telegram_gateway(req=req, user_container=user_container, chatbot_container=chatbot_container)


@app.route(route="processTempMessage", auth_level=func.AuthLevel.ANONYMOUS)
def processTempMessage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )


@app.route(route="chatbotv1", auth_level=func.AuthLevel.ANONYMOUS)
def chatbotv1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
            "Chatbotv1 called...",
            status_code=200
    )


@app.route(route="chatbotv2", auth_level=func.AuthLevel.ANONYMOUS)
def chatbotv2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return func.HttpResponse(
            "Chatbotv2 called...",
            status_code=200
    )