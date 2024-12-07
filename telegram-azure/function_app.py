# from azure.cosmos import CosmosClient
# from azure.cosmos import PartitionKey
from dotenv import load_dotenv
from azure.functions import FunctionApp, HttpRequest, HttpResponse, AuthLevel
from telegramClient import TelegramClient
import logging

# Instantiate function app
load_dotenv()
app = FunctionApp(http_auth_level=AuthLevel.ANONYMOUS)
# Instantiate cosmos db
# client = CosmosClient.from_connection_string(os.getenv("COSMOS_DB_CONNECTION_STRING"))
# user_database = client.create_database_if_not_exists("UserDB")
# user_container = user_database.create_container_if_not_exists(id="users", partition_key=PartitionKey(path="/user_uuid"))
# chatbot_database = client.create_database_if_not_exists("ChatbotDB")
# chatbot_container = chatbot_database.create_container_if_not_exists(id="chatbots", partition_key=PartitionKey(path="/chatbot_uuid"))


# Instantiate routes
@app.route(route="processTelegramMessage")
async def processTelegramMessage(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function "processTelegramMessage" processed a request.')
    # return await command_telegram_gateway(req=req, user_container=user_container, chatbot_container=chatbot_container)
    theClient = TelegramClient()
    return await theClient._process_message(req)



@app.route(route="processTempMessage", auth_level=AuthLevel.ANONYMOUS)
def processTempMessage(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )


@app.route(route="chatbotv1", auth_level=AuthLevel.ANONYMOUS)
def chatbotv1(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return HttpResponse(
            "Chatbotv1 called...",
            status_code=200
    )


@app.route(route="chatbotv2", auth_level=AuthLevel.ANONYMOUS)
def chatbotv2(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return HttpResponse(
            "Chatbotv2 called...",
            status_code=200
    )