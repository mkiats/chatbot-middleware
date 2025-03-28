from dataclasses import dataclass
import logging
from exceptions import EntityException
from typing import Optional, Dict, Union
from enum import Enum
from uuid import uuid4
import json
import time
import re

class ChatbotStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEBUG = "debug"

@dataclass
class DeploymentResource:
    deployment_type: str  # 'managed' or 'custom' or 'terraform'
    resource_group_name: str
    location: str = "southeastasia"
    subscription_id: Optional[str] = None
    app_insights_name: Optional[str] = None
    storage_account_name: Optional[str] = None

@dataclass
class DeploymentCredentials:
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None
    
class Chatbot:
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "placeholder name",
        version: str = "1.0.0",
        endpoint: str = "",
        description: str = "",
        status: ChatbotStatus = ChatbotStatus.INACTIVE,
        developer_id: Optional[str] = None,
        telegram_support: bool = False,
        deployment_resource: Optional[Union[Dict, DeploymentResource]] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None
    ):
        # Generate UUID if not provided
        self.id = str(id) if id else str(uuid4())
        
        # Validate endpoint format
        if endpoint=="" or not self._is_valid_endpoint(endpoint):
            raise EntityException(message="Valid endpoint URL is required", entity_type="Chatbot", field="endpoint")
            
        if len(name.strip()) == 0:
            raise EntityException(message="Chatbot name is required", entity_type="Chatbot", field="name")
        
        if isinstance(deployment_resource, dict):
            self.deployment_resource = deployment_resource
        elif isinstance(deployment_resource, DeploymentResource):
            self.deployment_resource = deployment_resource.__dict__
            
        # Set basic attributes
        self.version = version
        self.endpoint = endpoint
        self.name = name
        self.description = description
        self.status = status
        self.developer_id = developer_id
        self.telegram_support = telegram_support
        self.deployment_resource = deployment_resource
        
        # Set timestamps
        current_time = int(time.time())
        self.created_at = created_at if created_at else current_time
        self.updated_at = updated_at if updated_at else current_time

    @staticmethod
    def _is_valid_endpoint(endpoint: str) -> bool:
        """Validate endpoint URL format"""
        # TODO: Add endpoint validation method
        return True

    def validate(self) -> bool:
        """Validate chatbot attributes"""
        if not isinstance(self.id, str) or not self.id:
            raise EntityException("Invalid ID format", "Chatbot", "id")
            
        if not isinstance(self.version, str) or not self.version:
            raise EntityException("Invalid version format", "Chatbot", "version")
            
        if not self._is_valid_endpoint(self.endpoint):
            raise EntityException("Invalid endpoint URL", "Chatbot", "endpoint")
            
        if not isinstance(self.name, str) or not self.name:
            raise EntityException("Invalid chatbot name", "Chatbot", "name")
            
        if not isinstance(self.status, ChatbotStatus):
            raise EntityException("Invalid status", "Chatbot", "status")
            
        if self.developer_id and not isinstance(self.developer_id, str):
            raise EntityException("Invalid developer ID format", "Chatbot", "developer_id")
            
        if not isinstance(self.telegram_support, bool):
            raise EntityException("telegram_support must be boolean", "Chatbot", "telegram_support")
            
        return True

    def to_dict(self) -> Dict:
        """Convert chatbot object to dictionary representation"""
        return {
            "id": self.id,
            "version": self.version,
            "endpoint": self.endpoint,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "developer_id": self.developer_id,
            "telegram_support": self.telegram_support,
            "deployment_resource": self.deployment_resource,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def set_status(self, new_status: ChatbotStatus):
        """Update chatbot status"""
        if not isinstance(new_status, ChatbotStatus):
            raise EntityException("Invalid status value", "Chatbot", "status")
            
        self.status = new_status
        self.updated_at = int(time.time())
        self.validate()
    
    def set_name(self, new_name: str):
        strip_new_name = new_name.replace(" ", "-")
        pattern = re.compile(r'^[a-zA-Z0-9-]+$')
        if len(strip_new_name) == 0 or len(strip_new_name) >= 32 or not pattern.match(strip_new_name):
            raise EntityException("Invalid name value", "Chatbot", "name")
        self.name = strip_new_name
        self.updated_at = int(time.time())
        self.validate()

    
    def set_desc(self, new_desc: str):
        strip_new_desc = new_desc.replace(" ", "")
        if len(new_desc) == 0 or len(new_desc) >= 300 or not strip_new_desc.isalnum():
            raise EntityException("Invalid desc value", "Chatbot", "desc")
        self.description = new_desc
        self.updated_at = int(time.time())
        self.validate()

    def set_version(self, new_version: str):
        if len(new_version) == 0 or len(new_version) >= 10:
            raise EntityException("Invalid version value", "Chatbot", "version")
        self.version = new_version
        self.updated_at = int(time.time())
        self.validate()
    
    def set_telegram_support(self, new_telegram_support: bool):
        if not isinstance(new_telegram_support, bool):
            raise EntityException("Invalid telegram support value", "Chatbot", "telegram_support")
        self.telegram_support = new_telegram_support
        self.updated_at = int(time.time())
        self.validate()
        
    def validate_json(self):
        try:
            chatbot_dict = self.to_dict()
            json.dumps(chatbot_dict)
            return True
        except Exception as e:
            return False
        

    @classmethod
    def from_dict(cls, data: Dict) -> 'Chatbot':
        """Create chatbot object from dictionary data"""
        if not data:
            raise EntityException("Data dictionary is required", "Chatbot")
            
        try:
            return cls(
                id=data.get('id'),
                version=data.get('version', '1.0.0'),
                endpoint=data.get('endpoint', ''),
                name=data.get('name', ''),
                description=data.get('description', ''),
                status=ChatbotStatus(data.get('status', 'inactive')),
                developer_id=data.get('developer_id'),
                telegram_support=data.get('telegram_support', False),
                deployment_resource=data.get('deployment_resource'),
                created_at=data.get('created_at'),
                updated_at=data.get('updated_at')
            )
        except ValueError as e:
            raise EntityException(str(e), "Chatbot", "data_conversion")