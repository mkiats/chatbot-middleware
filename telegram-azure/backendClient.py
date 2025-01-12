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

    @staticmethod
    async def _activate_chatbot(req: HttpRequest) -> HttpResponse:
        db = CosmosDB()
        await db.initialize()
        try:
            # Get chatbot_uuid
            chatbot_id = req.params.get("chatbot_id", "")
            if not chatbot_id:
                raise BackendException(message=f"No chatbot id found in request parameters", method_name="_activate_chatbot")
            
            # Get chatbot
            the_chatbot_json = await query_by_key(container=db.chatbot_container, key="id", val=chatbot_id)
            if not the_chatbot_json:
                raise BackendException(message=f"No chatbot found with id {chatbot_id}", method_name="_activate_chatbot", error_code=BackendExceptionCode.NOT_FOUND)
            
            # Check status
            the_chatbot = Chatbot.from_dict(the_chatbot_json[0])

            if the_chatbot.status != 'active':
                the_chatbot.set_status(ChatbotStatus.ACTIVE)
                response = db.chatbot_container.upsert_item(body=the_chatbot.to_dict())
            return HttpResponse(
                body=json.dumps({"chatbot": the_chatbot.to_dict()}),
                mimetype="text/plain",
                status_code=200
            )
            
        except BackendException as backendException:
            return HttpResponse(
                    body=f"{backendException}",
                    mimetype="text/plain",
                    status_code=backendException.get_status_code()
                )
        
        except Exception as e:
            logging.error("Error occured in _activate_chatbot")
            return HttpResponse(
                    body=f"Error processing _activate_chatbot, {e}",
                    mimetype="text/plain",
                    status_code=500
                )

    @staticmethod
    async def _deactivate_chatbot(req: HttpRequest) -> HttpResponse:
        db = CosmosDB()
        await db.initialize()
        try:
            # Get chatbot_uuid
            chatbot_id = req.params.get("chatbot_id", "")
            if not chatbot_id:
                raise BackendException(message=f"No chatbot id found in request parameters", method_name="_deactivate_chatbot")
            
            # Get chatbot
            the_chatbot_json = await query_by_key(container=db.chatbot_container, key="id", val=chatbot_id)
            if not the_chatbot_json:
                raise BackendException(message=f"No chatbot found with id {chatbot_id}", method_name="_deactivate_chatbot", error_code=BackendExceptionCode.NOT_FOUND)
            
            # Check status
            the_chatbot = Chatbot.from_dict(the_chatbot_json[0])

            if the_chatbot.status != 'inactive':
                the_chatbot.set_status(ChatbotStatus.INACTIVE)
                response = db.chatbot_container.upsert_item(body=the_chatbot.to_dict())
            return HttpResponse(
                body=json.dumps({"chatbot": the_chatbot.to_dict()}),
                mimetype="text/plain",
                status_code=200
            )
            
        except BackendException as backendException:
            return HttpResponse(
                    body=f"{backendException}",
                    mimetype="text/plain",
                    status_code=backendException.get_status_code()
                )
        
        except Exception as e:
            return HttpResponse(
                    body=f"Error processing _deactivate_chatbot, {e}",
                    mimetype="text/plain",
                    status_code=500
                )

    @staticmethod
    async def _update_chatbot(req: HttpRequest) -> HttpResponse:
        db = CosmosDB()
        await db.initialize()
        try:
            # Get chatbot_uuid
            chatbot_id = req.params.get("chatbot_id", "")
            if not chatbot_id:
                raise BackendException(message=f"No chatbot id found in request parameters", method_name="_update_chatbot")
            # Get chatbot
            the_chatbot_json = await query_by_key(container=db.chatbot_container, key="id", val=chatbot_id)
            if not the_chatbot_json:
                raise BackendException(message=f"No chatbot found with id {chatbot_id}", method_name="_update_chatbot", error_code=BackendExceptionCode.NOT_FOUND)
            
            # Check status
            the_chatbot = Chatbot.from_dict(the_chatbot_json[0])

            try:
                if req.get_json().get("chatbot_name", ""):
                    new_name = req.get_json().get("chatbot_name", "")
                    the_chatbot.set_name(new_name=new_name)
                if req.get_json().get("chatbot_desc", ""):
                    the_chatbot.set_desc(req.get_json().get("chatbot_desc"))
                if req.get_json().get("chatbot_status", ""):
                    the_chatbot.set_status(ChatbotStatus(req.get_json().get("chatbot_status")))
                if req.get_json().get("chatbot_version", ""):
                    the_chatbot.set_version(req.get_json().get("chatbot_version"))
                if isinstance(req.get_json().get("chatbot_telegram_support", ""), bool):
                    the_chatbot.set_telegram_support(req.get_json().get("chatbot_telegram_support"))
                response = db.chatbot_container.upsert_item(body=the_chatbot.to_dict())
            except Exception as e:
                raise BackendException(message=f"Invalid chatbot parameters,  {e}", method_name="_update_chatbot")
            
            if the_chatbot.validate_json():
                return HttpResponse(
                    body=json.dumps({"chatbot": the_chatbot.to_dict()}),
                    mimetype="application/json",
                    status_code=200
                )
            else:
                raise BackendException(message=f"Chatbot.to_dict() not json serialisable", method_name="_update_chatbot")
            
        except BackendException as backendException:
            return HttpResponse(
                    body=f"{backendException}",
                    mimetype="text/plain",
                    status_code=backendException.get_status_code()
                )
        
        except Exception as e:
            return HttpResponse(
                    body=f"Error processing _update_chatbot, {e}",
                    mimetype="text/plain",
                    status_code=500
                )