from _common import _command_mapper
from typing import Optional
from uuid import uuid4
import json
import time
import re

# def callback_data_chatbot(chatbot_uuid: str):
#     return {
#         'command': 'command_callback_selectChatbot',
#         'chatbot_uuid': chatbot_uuid
#     }

class User:
    def __init__(self, user_uuid: str, selected_chatbot: str, updated_at: str):
        self.user_uuid = str(user_uuid) if user_uuid != "" else str(uuid4())
        self.id = str(self.user_uuid)
        self.selected_chatbot = selected_chatbot
        self.updated_at = updated_at if updated_at != "" else int(time.time())


    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_uuid": str(self.user_uuid),
            "selected_chatbot": self.selected_chatbot,
            "updated_at": self.updated_at
        }

class ChatbotCallbackData:
    def __init__(self, command: str, chatbot_uuid: str):
        self.command = command
        self.chatbot_uuid = chatbot_uuid
        self.shortened = f'{_command_mapper(self.command, False)}_{self.chatbot_uuid}'
    
    def to_callback_string(self) -> str:
        return self.shortened


class Chatbot:
    def __init__(self, chatbot_uuid: str, chatbot_name: str, chatbot_endpoint: str, chatbot_status: str):
        self.chatbot_uuid = chatbot_uuid
        self.chatbot_name = chatbot_name
        self.chatbot_endpoint = chatbot_endpoint
        self.chatbot_status = chatbot_status

    def __post_init__(self):
        self.validate()
    
    def validate(self) -> bool:
        # Populate with custom error exceptions, throw customException when necessary
        # Need to handle chatbot_uuid should be UUID format, endpoint needs to be valid
            
        if self.status not in ['active', 'maintenance', 'deprecated', 'debug']:
            raise ValueError("status must be one of: active, maintenance, deprecated, debug")
            
        return True
    
    def to_dict(self) -> dict:
        return {
            "chatbot_uuid": self.chatbot_uuid,
            "chatbot_name": self.chatbot_name,
            "chatbot_endpoint": self.chatbot_endpoint,
            "chatbot_status": self.chatbot_status
        }
    
class inline_keyboard_button:
    def __init__(self, text: str, callback_data: str = None):
        self.text = text
        self.callback_data = callback_data

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "callback_data": self.callback_data
        }
    