from enum import Enum
from typing import Optional, Dict, Any


class ChatbotValidationError(Exception):
    """Custom exception for chatbot validation errors"""
    pass


class DeploymentExceptionCode(Enum):
    DEFAULT = "DP400"


class DeploymentException(Exception):
    def __init__(
        self, 
        message: str,
        deployment_stage: str,
        error_code: DeploymentExceptionCode = DeploymentExceptionCode.DEFAULT,
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
    

class EntityExceptionCode(Enum):
    DEFAULT = "EN400"
    INVALID_FIELD = "EN422"
    DUPLICATE = "EN409"

class EntityException(Exception):
    def __init__(
        self, 
        message: str,
        entity_type: str,
        error_code: EntityExceptionCode = EntityExceptionCode.DEFAULT,
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

class BackendExceptionCode(Enum):
    DEFAULT = "BE400"
    FORBIDDEN = "BE403"
    NOT_FOUND = "BE404"
    INVALID_FIELD = "BE422"
    DUPLICATE = "BE409"

class BackendException(Exception):
    def __init__(
        self, 
        message: str,
        method_name: str,
        error_code: BackendExceptionCode = BackendExceptionCode.DEFAULT,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.method_name = method_name
        self.field = field
        self.message = message
        self.error_code = error_code
        self.status_code = int(self.error_code.value[-3:-1])
        self.details = details or {}
        
        self._formatted_message = (
            f"Error Code: {self.error_code.value} \nMethod name: {self.method_name} \nError Msg: {self.message}"
            + (f"\nField: {self.field}" if self.field else "")
        )
        super().__init__(self._formatted_message)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize error for API responses"""
        error_dict = {
            "code": self.error_code.value,
            "method_name": self.method_name,
            "message": self.message,
            "details": self.details
        }
        if self.field:
            error_dict["field"] = self.field
        return error_dict

    def get_status_code(self):
        return self.status_code

class TelegramExceptionCode(Enum):
    DEFAULT = "TE400"
    FORBIDDEN = "TE403"
    NOT_FOUND = "TE404"
    INVALID_FIELD = "TE422"
    DUPLICATE = "TE409"

class TelegramException(Exception):
    def __init__(
        self, 
        message: str,
        method_name: str,
        error_code: TelegramExceptionCode = TelegramExceptionCode.DEFAULT,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.method_name = method_name
        self.field = field
        self.message = message
        self.error_code = error_code
        self.status_code = int(self.error_code.value[-3:-1])
        self.details = details or {}
        
        self._formatted_message = (
            f"Error Code: {self.error_code.value} \nMethod name: {self.method_name} \nError Msg: {self.message}"
            + (f"\nField: {self.field}" if self.field else "")
        )
        super().__init__(self._formatted_message)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize error for API responses"""
        error_dict = {
            "code": self.error_code.value,
            "method_name": self.method_name,
            "message": self.message,
            "details": self.details
        }
        if self.field:
            error_dict["field"] = self.field
        return error_dict

    def get_status_code(self):
        return self.status_code