import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import InfrastructureRequest, DeploymentResponse
from .terraform_manager import TerraformManager
from pathlib import Path
import os
import json
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Infrastructure Deployment Service", debug=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Template directory configuration
load_dotenv()
TEMPLATE_DIR = "./app/terraform" # os.getenv("TEMPLATE_DIR", "./app/terraform")
logging.info(f"Template_dir: {TEMPLATE_DIR}")
logging.info(f"Current dir: {os.getcwd()}")
logging.info(f'{os.listdir(TEMPLATE_DIR)}')

@app.post("/deploy/infrastructure", response_model=DeploymentResponse)
async def deploy_infrastructure(request: InfrastructureRequest) -> DeploymentResponse:
    request = request.dict()
    logging.warning(json.dumps(request))
    """
    Deploy infrastructure using Terraform based on the provided configuration
    """
    tf_manager = None
    auto_approve = True
    try:
        tf_manager = TerraformManager(template_dir=TEMPLATE_DIR)
        
        # Setup workspace with template files
        await tf_manager.setup_workspace()
        
        # Create tfvars file
        await tf_manager.create_tfvars(request)
        
        # Initialize Terraform
        success, output = await tf_manager.init()
        if not success:
            raise HTTPException(status_code=500, detail=f"Terraform init failed: {output}")
        
        # Run plan
        success, plan_output = await tf_manager.plan()
        if not success:
            raise HTTPException(status_code=500, detail=f"Terraform plan failed: {plan_output}")
        
        # Run apply
        success, apply_output = await tf_manager.apply(auto_approve=auto_approve)
        if not success:
            raise HTTPException(status_code=500, detail=f"Terraform apply failed: {apply_output}")
        
        return DeploymentResponse(
            success=True,
            message="Infrastructure deployed successfully",
            details=apply_output
        )
        
    except Exception as e:
        logger.error(f"Deployment failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if tf_manager:
            await tf_manager.cleanup()

# Health check endpoint
@app.get("/health")
async def health_check():
    logging.warning("Status check executed...")
    return {"status": "healthy"}