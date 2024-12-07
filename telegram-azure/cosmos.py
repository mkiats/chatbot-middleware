from azure.cosmos import CosmosClient, ContainerProxy, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError
from typing import List, Dict, Any, Optional
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
            partition_key=PartitionKey(path="/user_uuid")
        )
        self._chatbot_container = chatbot_db.create_container_if_not_exists(
            id="chatbots", 
            partition_key=PartitionKey(path="/chatbot_uuid")
        )

    @property
    def user_container(self) -> ContainerProxy:
        return self._user_container

    @property 
    def chatbot_container(self) -> ContainerProxy:
        return self._chatbot_container


def query_by_key(container: ContainerProxy, key: str) -> List[Dict[str, Any]]:
    try:
        # Using parameterized query for security
        query = "SELECT * FROM c WHERE c.id = @key"
        params = [dict(name="@key", value=key)]
        
        item = list(container.query_items(
            query=query,
            parameters=params,
            enable_cross_partition_query=True
        ))
        
        return item
        
    except CosmosHttpResponseError as e:
        print(f"Cosmos DB query error: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise