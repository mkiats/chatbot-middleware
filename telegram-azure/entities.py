from dataclasses import dataclass
from _common import _command_mapper
from exceptions import EntityError
from typing import Optional, Dict, Union
from enum import Enum
from uuid import uuid4
import json
import time
import re
import bcrypt


class UserRole(Enum):
    ADMIN = "Admin"
    DEVELOPER = "Developer"
    USER = "User"

class User:
    def __init__(
        self,
        id: None,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        role: UserRole = UserRole.USER,
        selected_chatbot_id: Optional[str] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None
    ):  
        if role!=UserRole.USER:
            # Validate full name
            if not full_name or len(full_name.strip()) == 0:
                raise EntityError("Full name is required", "User", "full_name")
            # Validate email
            if not email:
                raise EntityError("Email is required", "User", "email")
            if '@' not in email:
                raise EntityError("Invalid email format", "User", "email")
            # Validate password
            if not password:
                raise EntityError("Password is required", "User", "password")
            if len(password) < 8:
                raise EntityError("Password must be at least 8 characters", "User", "password")
            email=email.lower()
            password=bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
        
        self.id = str(id) if id else str(uuid4())
        self.partition = self.id[:4]
        self.full_name = full_name
        self.email = email
        self.password_hash = password
        self.role = role
        self.selected_chatbot_id = selected_chatbot_id
        current_time = int(time.time())
        self.created_at = created_at if created_at else current_time
        self.updated_at = updated_at if updated_at else current_time

    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches stored hash"""
        if not password:
            raise EntityError("Password is required", "User", "password")
            
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def update_password(self, new_password: str) -> None:
        """Update user's password with a new one"""
        if not new_password:
            raise EntityError("New password is required", "User", "password")
        if len(new_password) < 8:
            raise EntityError("Password must be at least 8 characters", "User", "password")
            
        self.password_hash = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        self.updated_at = int(time.time())

    def to_dict(self) -> Dict:
        """Convert user object to dictionary representation"""
        return {
            "id": str(self.id),
            "partition": self.partition,
            "full_name": self.full_name,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role.value,
            "selected_chatbot_id": self.selected_chatbot_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create user object from dictionary data"""
        if not data:
            raise EntityError("Data dictionary is required", "User")
            
        try:
            return cls(
                id=data.get('id'),
                full_name=data.get('full_name', ''),
                email=data.get('email', ''),
                selected_chatbot_id=data.get('selected_chatbot_id'),
                role=UserRole(data.get('role', 'Developer')),  # Fixed: was using user_group instead of role
                created_at=data.get('created_at'),
                updated_at=data.get('updated_at')
            )
        except ValueError as e:
            raise EntityError(str(e), "User", "from_dict method")


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
        name: str = "placeholder_name",
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
            raise EntityError(message="Valid endpoint URL is required", entity_type="Chatbot", field="endpoint")
            
        if len(name.strip()) == 0:
            raise EntityError(message="Chatbot name is required", entity_type="Chatbot", field="name")
        
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
            raise EntityError("Invalid ID format", "Chatbot", "id")
            
        if not isinstance(self.version, str) or not self.version:
            raise EntityError("Invalid version format", "Chatbot", "version")
            
        if not self._is_valid_endpoint(self.endpoint):
            raise EntityError("Invalid endpoint URL", "Chatbot", "endpoint")
            
        if not isinstance(self.name, str) or not self.name:
            raise EntityError("Invalid chatbot name", "Chatbot", "name")
            
        if not isinstance(self.status, ChatbotStatus):
            raise EntityError("Invalid status", "Chatbot", "status")
            
        if self.developer_id and not isinstance(self.developer_id, str):
            raise EntityError("Invalid developer ID format", "Chatbot", "developer_id")
            
        if not isinstance(self.telegram_support, bool):
            raise EntityError("telegram_support must be boolean", "Chatbot", "telegram_support")
            
        return True

    def to_dict(self) -> Dict:
        """Convert chatbot object to dictionary representation"""
        return {
            "id": str(self.id),
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
            raise EntityError("Invalid status value", "Chatbot", "status")
            
        self.status = new_status
        self.updated_at = int(time.time())
        self.validate()

    @classmethod
    def from_dict(cls, data: Dict) -> 'Chatbot':
        """Create chatbot object from dictionary data"""
        if not data:
            raise EntityError("Data dictionary is required", "Chatbot")
            
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
            raise EntityError(str(e), "Chatbot", "data_conversion")

class ChatbotCallbackData:
    @staticmethod
    def create_callback_str(command: str, chatbot_id: str):
       return f'{_command_mapper(command, False)}_{chatbot_id}'

    @staticmethod
    def destructure_callback_str(callback_string: str) -> tuple[str, str]:
        [short_command_str, chatbot_id] = callback_string.split('_', maxsplit=1)
        return short_command_str, chatbot_id

class inline_keyboard_button:
    def __init__(self, text: str, callback_data: str = None):
        self.text = text
        self.callback_data = callback_data

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "callback_data": self.callback_data
        }
    