import logging
from typing import Tuple
from azure.cosmos import ContainerProxy
from azure.functions import HttpResponse, HttpRequest
from cosmos import CosmosDB, query_by_key, query_by_sql
from entities import Chatbot
import json

class BackendClient:
    @staticmethod
    async def _get_all_chatbots(req: HttpRequest) -> HttpResponse:
        try:
            db = CosmosDB()
            await db.initialize()
            query = "SELECT * FROM c"
            results = await query_by_sql(container=db.chatbot_container, queryStr=query)

            return HttpResponse(
                body=json.dumps(results),
                mimetype="application/json",
                status_code=200
            )
        except Exception as e:
            return HttpResponse(
                    body="Error processing _activate_chatbot",
                    mimetype="text/plain",
                    status_code=500
                )

    @staticmethod
    async def _activate_chatbot(req: HttpRequest) -> HttpResponse:
        db = CosmosDB()
        await db.initialize()
        try:
            # Get chatbot_uuid
            chatbot_uuid = req.route_params.get('chatbot_uuid')
            logging.warning(chatbot_uuid)
            if not chatbot_uuid:
                return HttpResponse(
                    body="Missing chatbot ID",
                    mimetype="text/plain",
                    status_code=400
                )
            
            # Get chatbot
            the_chatbot = await query_by_key(container=db.chatbot_container, key=chatbot_uuid)
            logging.warning(the_chatbot)
            if not the_chatbot:
                return HttpResponse(
                    body="Invalid Chatbot ID",
                    mimetype="text/plain",
                    status_code=400
                )
            
            # Check status
            the_chatbot_name = the_chatbot[0].get("chatbot_name")
            the_chatbot_status = the_chatbot[0].get("chatbot_status")
            the_chatbot_endpoint = the_chatbot[0].get("chatbot_endpoint")
            logging.warning(the_chatbot_name)
            logging.warning(the_chatbot_status)
            logging.warning(the_chatbot_endpoint)

            if the_chatbot_status == 'active':
                return HttpResponse(
                    body="Chatbot is already active",
                    mimetype="text/plain",
                    status_code=200
                )
            else:
                updated_chatbot = Chatbot(chatbot_uuid=chatbot_uuid, chatbot_endpoint=the_chatbot_endpoint, chatbot_name=the_chatbot_name, chatbot_status=the_chatbot_status)
                updated_chatbot.set_status("active")
                logging.warning("testt")
                logging.warning(updated_chatbot)
                response = db.chatbot_container.upsert_item(body=updated_chatbot.to_dict())
                return HttpResponse(
                    body=f"Chatbot successfully activated",
                    mimetype="text/plain",
                    status_code=200
                )
        
        except Exception as e:
            return HttpResponse(
                    body="Error processing _activate_chatbot",
                    mimetype="text/plain",
                    status_code=500
                )




    @staticmethod
    async def _deactivate_chatbot(req: HttpRequest) -> HttpResponse:
        db = CosmosDB()
        await db.initialize()
        try:
            # Get chatbot_uuid
            chatbot_uuid = req.route_params.get('chatbot_uuid')
            logging.warning(chatbot_uuid)
            if not chatbot_uuid:
                return HttpResponse(
                    body="Missing chatbot ID",
                    mimetype="text/plain",
                    status_code=400
                )
            
            # Get chatbot
            the_chatbot = await query_by_key(container=db.chatbot_container, key=chatbot_uuid)
            logging.warning(the_chatbot)
            if not the_chatbot:
                return HttpResponse(
                    body="Invalid Chatbot ID",
                    mimetype="text/plain",
                    status_code=400
                )
            
            # Check status
            the_chatbot_name = the_chatbot[0].get("chatbot_name")
            the_chatbot_status = the_chatbot[0].get("chatbot_status")
            the_chatbot_endpoint = the_chatbot[0].get("chatbot_endpoint")
            logging.warning(the_chatbot_name)
            logging.warning(the_chatbot_status)
            logging.warning(the_chatbot_endpoint)

            if the_chatbot_status == 'inactive':
                return HttpResponse(
                    body="Chatbot is already inactive",
                    mimetype="text/plain",
                    status_code=200
                )
            else:
                updated_chatbot = Chatbot(chatbot_uuid=chatbot_uuid, chatbot_endpoint=the_chatbot_endpoint, chatbot_name=the_chatbot_name, chatbot_status=the_chatbot_status)
                updated_chatbot.set_status("inactive")
                logging.warning("testt")
                logging.warning(updated_chatbot)
                response = db.chatbot_container.upsert_item(body=updated_chatbot.to_dict())
                return HttpResponse(
                    body=f"Chatbot successfully deactivated",
                    mimetype="text/plain",
                    status_code=200
                )
        
        except Exception as e:
            return HttpResponse(
                    body="Error processing _deactivate_chatbot",
                    mimetype="text/plain",
                    status_code=500
                )
    
