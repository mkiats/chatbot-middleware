from enum import Enum
from typing import Optional, Dict, Any


class ChatbotValidationError(Exception):
    """Custom exception for chatbot validation errors"""
    pass


class DeploymentErrorCode(Enum):
    DEFAULT = "Deployment 400"


class DeploymentError(Exception):
    def __init__(
        self, 
        message: str,
        deployment_stage: str,
        error_code: DeploymentErrorCode = DeploymentErrorCode.DEFAULT,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.deployment_stage = deployment_stage
        self.field = field
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        
        self._formatted_message = (
            f"Error Code: {self.error_code.value} \nDeployment Stage: {self.deployment_stage} \nError Msg: {self.message}"
            + (f"\nField: {self.field}" if self.field else "")
        )
        super().__init__(self._formatted_message)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize error for API responses"""
        error_dict = {
            "code": self.error_code.value,
            "type": self.deployment_stage,
            "message": self.message,
            "details": self.details
        }
        if self.field:
            error_dict["field"] = self.field
        return error_dict
    

class EntityErrorCode(Enum):
    DEFAULT = "Entity400"
    INVALID_FIELD = "Entity422"
    DUPLICATE = "Entity409"

class EntityError(Exception):
    def __init__(
        self, 
        message: str,
        entity_type: str,
        error_code: EntityErrorCode = EntityErrorCode.DEFAULT,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.entity_type = entity_type
        self.field = field
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        
        self._formatted_message = (
            f"Error Code: {self.error_code.value} \nEntity type: {self.entity_type} \nError Msg: {self.message}"
            + (f"\nField: {self.field}" if self.field else "")
        )
        super().__init__(self._formatted_message)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize error for API responses"""
        error_dict = {
            "code": self.error_code.value,
            "type": self.entity_type,
            "message": self.message,
            "details": self.details
        }
        if self.field:
            error_dict["field"] = self.field
        return error_dict