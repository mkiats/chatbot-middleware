from typing import Optional
from uuid import UUID
import re

# def callback_data_chatbot(chatbot_uuid: str):
#     return {
#         'command': 'command_callback_selectChatbot',
#         'chatbot_uuid': chatbot_uuid
#     }


class ChatbotCallbackData:
    def __init__(self, command: str, chatbot_uuid: str):
        self.command = command
        self.chatbot_uuid = chatbot_uuid
        
    def to_dict(self) -> dict:
        return vars(self)


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
            
        if self.status not in ['active', 'maintenance', 'deprecated']:
            raise ValueError("status must be one of: active, maintenance, deprecated")
            
        return True
    
    def to_dict(self) -> dict:
        return vars(self)
    
class inline_keyboard_button:
    def __init__(self, text: str, callback_data: ChatbotCallbackData = None):
        self.text = text
        self.callback_data = ChatbotCallbackData

    def to_dict(self) -> dict:
        return vars(self)
    