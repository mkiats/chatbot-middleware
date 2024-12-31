from enum import Enum
from typing import Optional, Dict


class ChatbotValidationError(Exception):
    """Custom exception for chatbot validation errors"""
    pass

class EntityError(Exception):
    def __init__(self, message: str, entity_type: str, field: Optional[str] = None):
        self.entity_type = entity_type
        self.field = field
        self.message = message
        self._formatted_message = (
            f"{self.entity_type} Error: {self.message} (Field: {self.field})"
            if self.field
            else f"{self.entity_type} Error: {self.message}"
        )
        super().__init__(self._formatted_message)

    @property
    def formatted_message(self) -> str:
        return self._formatted_message

