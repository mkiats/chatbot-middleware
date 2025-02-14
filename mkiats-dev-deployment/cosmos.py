import logging
from azure.cosmos import CosmosClient, ContainerProxy, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError
from typing import List, Dict, Any
import os

class CosmosDB:
    def __init__(self):
        self._client = CosmosClient.from_connection_string(os.getenv("COSMOS_DB_CONNECTION_STRING"))
        self._user_container = None
        self._chatbot_container = None

    async def initialize(self):
        user_db = self._client.create_database_if_not_exists("UserDB")
        chatbot_db = self._client.create_database_if_not_exists("ChatbotDB")
        
        self._user_container = user_db.create_container_if_not_exists(
            id="users",
            partition_key=PartitionKey(path="/partition")
        )
        self._chatbot_container = chatbot_db.create_container_if_not_exists(
            id="chatbots", 
            partition_key=PartitionKey(path="/developer_id")
        )

    @property
    def user_container(self) -> ContainerProxy:
        return self._user_container

    @property 
    def chatbot_container(self) -> ContainerProxy:
        return self._chatbot_container


async def query_by_key(container: ContainerProxy, key: str, val: str) -> List[Dict[str, Any]]:
    try:
        query = f"SELECT * FROM c WHERE c.{key} = @{key}"
        params = [dict(name=f"@{key}", value=str(val))]
        
        items = list(container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))
        return items
        
    except CosmosHttpResponseError as e:
        logging.error(f"Cosmos DB query error: {str(e)}")
        raise
    except Exception as e:
        logging.error(str(e))
        raise

async def query_by_sql(container: ContainerProxy, queryStr: str) -> List[Dict[str, Any]]:
    try:
        results = list(container.query_items(
            query=queryStr,             
            enable_cross_partition_query=True
        )
    )
        return results
    except CosmosHttpResponseError as e:
        logging.error(f"Cosmos DB query error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise