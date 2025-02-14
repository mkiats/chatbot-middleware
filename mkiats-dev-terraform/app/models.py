from pydantic import BaseModel
from typing import Dict, Any
from enum import Enum

class TerraformStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class InfrastructureRequest(BaseModel):
    name: str
    version: str
    description: str
    status: str
    developer_id: str
    telegram_support: bool
    deployment_type: str
    subscription_id: str
    location: str
    resource_group_name: str
    app_insights_name: str
    storage_account_name: str
    client_id: str
    client_secret: str
    tenant_id: str
    
    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        return super().dict(*args, **kwargs)


class DeploymentResponse(BaseModel):
    success: bool
    message: str
    details: str