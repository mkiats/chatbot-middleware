import logging
from typing import Tuple
from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse, HttpRequest
from cosmos import CosmosDB, query_by_key, query_by_sql
from entities import Chatbot, ChatbotStatus
from exceptions import BackendException, BackendExceptionCode
import json

# TODO: Edit backend commands

class BackendClient:

    @staticmethod
    async def _get_chatbots_by_sql(req: HttpRequest) -> HttpResponse:
        # SQL Query passed via request body
        try:
            db = CosmosDB()
            await db.initialize()
            query = req.get_json().get("query", "")
            if query:
                results = await query_by_sql(container=db.chatbot_container, queryStr=query)

            return HttpResponse(
                
                body=json.dumps({"chatbots": results}),
                mimetype="application/json",
                status_code=200
            )
        except Exception as e:
            logging.error("Error occured in _run_sql_query")
            return HttpResponse(
                    body=f"Error processing _get_chatbots_by_sql, {e}",
                    mimetype="text/plain",
                    status_code=500
            )

    @staticmethod
    async def _get_chatbots(req: HttpRequest) -> HttpResponse:
        # Parameters passed via REQUEST PARAMS (NOTE: NOT REQUEST ROUTE PARAMETERS)
        try:
            db = CosmosDB()
            await db.initialize()
            dev_id = req.params.get("developer_id", "")
            chatbot_id = req.params.get("chatbot_id", "")

            if len(req.params) == 0:
                query = "SELECT * FROM c"
                chatbots_result = await query_by_sql(container=db.chatbot_container, queryStr=query)
            elif dev_id:
                chatbots_result = await query_by_key(container=db.chatbot_container, key="developer_id", val=str(dev_id))
            elif chatbot_id:
                chatbots_result = await query_by_key(container=db.chatbot_container, key="id", val=str(chatbot_id))
            else:
                raise BackendException(message=f"Invalid request parameters", method_name="_get_chatbots", error_code=BackendExceptionCode.FORBIDDEN) 
            
            return HttpResponse(
                body=json.dumps({"chatbots": chatbots_result}),
                mimetype="application/json",
                status_code=200
            )
        except BackendException as backendException:
            return HttpResponse(
                    body=f"Error processing _get_all_chatbot, {backendException}",
                    mimetype="text/plain",
                    status_code=backendException.get_status_code()
                )

        except Exception as e:
            logging.error("Error occured in _get_all_chatbot")
            return HttpResponse(
                    body=f"Error processing _get_all_chatbot, {e}",
                    mimetype="text/plain",
                    status_code=400
                )