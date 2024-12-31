from _common import _command_mapper
from exceptions import EntityError
from typing import Optional, Enum, Dict
from uuid import uuid4
import json
import time
import re
import bcrypt

# def callback_data_chatbot(chatbot_uuid: str):
#     return {
#         'command': 'command_callback_selectChatbot',
#         'chatbot_uuid': chatbot_uuid
#     }


class UserRole(Enum):
    ADMIN = "Admin"
    DEVELOPER = "Developer" 

class User:
    def __init__(
        self,
        uuid: Optional[str] = None,
        full_name: str = "placeholder name",
        email: str = "placeholder email",
        password: str = "placeholder password",
        role: UserRole = UserRole.DEVELOPER,
        selected_chatbot_uuid: Optional[str] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None
    ):
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
        
        self.uuid = str(uuid) if uuid else str(uuid4())
        self.partition = self.uuid[:4]  # Fixed: was using user_uuid instead of uuid
        self.full_name = full_name
        self.email = email.lower()
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        self.role = role
        self.selected_chatbot_uuid = selected_chatbot_uuid
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
            "uuid": str(self.uuid),
            "partition": self.partition,
            "full_name": self.full_name,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role.value,
            "selected_chatbot_uuid": self.selected_chatbot_uuid,
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
                uuid=data.get('uuid'),
                full_name=data.get('full_name', ''),
                email=data.get('email', ''),
                selected_chatbot_uuid=data.get('selected_chatbot_uuid'),
                role=UserRole(data.get('role', 'Developer')),  # Fixed: was using user_group instead of role
                created_at=data.get('created_at'),
                updated_at=data.get('updated_at')
            )
        except ValueError as e:
            raise EntityError(str(e), "User", "from_dict method")


# class Chatbot:
#     def __init__(self, chatbot_uuid: str, chatbot_name: str, chatbot_endpoint: str, chatbot_status: str):
#         self.chatbot_uuid = str(chatbot_uuid) if chatbot_uuid != "" else str(uuid4())
#         self.id = str(self.chatbot_uuid)
#         self.chatbot_name = chatbot_name
#         self.chatbot_endpoint = chatbot_endpoint
#         self.chatbot_status = chatbot_status

#     def __post_init__(self):
#         self.validate()
    
#     def validate(self) -> bool:
#         # Populate with custom error exceptions, throw customException when necessary
#         # Need to handle chatbot_uuid should be UUID format, endpoint needs to be valid
            
#         if self.chatbot_status not in ['active', 'inactive', 'deprecated', 'debug']:
#             raise ValueError("status must be one of: active, inactive, deprecated, debug")
            
#         return True
    
#     def to_dict(self) -> dict:
#         return {
#             "id": self.id,
#             "chatbot_uuid": self.chatbot_uuid,
#             "chatbot_name": self.chatbot_name,
#             "chatbot_endpoint": self.chatbot_endpoint,
#             "chatbot_status": self.chatbot_status
#         }
    
#     def set_status(self, new_status: str):
#         self.chatbot_status = new_status
#         self.validate()


class ChatbotStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEBUG = "debug"

class Chatbot:
    def __init__(
        self,
        uuid: Optional[str] = None,
        name: str = "placeholder_name",
        version: str = "1.0.0",
        endpoint: str = "",
        description: str = "",
        status: ChatbotStatus = ChatbotStatus.INACTIVE,
        developer_uuid: Optional[str] = None,
        telegram_support: bool = False,
        deployment_resource: Optional[str] = None,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None
    ):
        # Generate UUID if not provided
        self.uuid = str(uuid) if uuid else str(uuid4())
        
        # Validate endpoint format
        if not endpoint or not self._is_valid_endpoint(endpoint):
            raise EntityError("Valid endpoint URL is required", "Chatbot", "endpoint")
            
        if not name or len(name.strip()) == 0:
            raise EntityError("Chatbot name is required", "Chatbot", "name")
            
        # Set basic attributes
        self.version = version
        self.endpoint = endpoint
        self.name = name
        self.description = description
        self.status = status
        self.developer_uuid = developer_uuid
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
        if not isinstance(self.uuid, str) or not self.uuid:
            raise EntityError("Invalid UUID format", "Chatbot", "uuid")
            
        if not isinstance(self.version, str) or not self.version:
            raise EntityError("Invalid version format", "Chatbot", "version")
            
        if not self._is_valid_endpoint(self.endpoint):
            raise EntityError("Invalid endpoint URL", "Chatbot", "endpoint")
            
        if not isinstance(self.name, str) or not self.name:
            raise EntityError("Invalid chatbot name", "Chatbot", "name")
            
        if not isinstance(self.status, ChatbotStatus):
            raise EntityError("Invalid status", "Chatbot", "status")
            
        if self.developer_uuid and not isinstance(self.developer_uuid, str):
            raise EntityError("Invalid developer UUID format", "Chatbot", "developer_uuid")
            
        if not isinstance(self.telegram_support, bool):
            raise EntityError("telegram_support must be boolean", "Chatbot", "telegram_support")
            
        return True

    def to_dict(self) -> Dict:
        """Convert chatbot object to dictionary representation"""
        return {
            "uuid": str(self.uuid),
            "version": self.version,
            "endpoint": self.endpoint,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "developer_uuid": self.developer_uuid,
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
                uuid=data.get('uuid'),
                version=data.get('version', '1.0.0'),
                endpoint=data.get('endpoint', ''),
                name=data.get('name', ''),
                description=data.get('description', ''),
                status=ChatbotStatus(data.get('status', 'inactive')),
                developer_uuid=data.get('developer_uuid'),
                telegram_support=data.get('telegram_support', False),
                deployment_resource=data.get('deployment_resource'),
                created_at=data.get('created_at'),
                updated_at=data.get('updated_at')
            )
        except ValueError as e:
            raise EntityError(str(e), "Chatbot", "data_conversion")

class ChatbotCallbackData:
    #TODO: Remove init method and change to creation and destructuring of callback data to 2 static methods
    def __init__(self, command: str, chatbot_uuid: str):
        self.command = command
        self.chatbot_uuid = chatbot_uuid
        self.shortened = f'{_command_mapper(self.command, False)}_{self.chatbot_uuid}'
    
    def to_callback_string(self) -> str:
        return self.shortened

class inline_keyboard_button:
    def __init__(self, text: str, callback_data: str = None):
        self.text = text
        self.callback_data = callback_data

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "callback_data": self.callback_data
        }
    