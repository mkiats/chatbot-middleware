import asyncio
from typing import Any, AsyncGenerator, Dict, Generator
from dotenv import load_dotenv
from backendClient import BackendClient
from azureFunctionDeployerClient import AzureFunctionDeployerClient
from terraformClient import TerraformExecutor
from entities import TerraformStatus
import azure.functions as func
import azure.durable_functions as df
import logging
import json
from chatbot import main

# Instantiate function app
load_dotenv()
app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="chatbots", auth_level=func.AuthLevel.ANONYMOUS)
async def get_chatbots(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient._get_chatbots(req)


@app.route(route="chatbots/deploy/validate", auth_level=func.AuthLevel.ANONYMOUS)
async def deploy_chatbot_validate(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('deploy_chatbot_validate executed...')
    theClient = AzureFunctionDeployerClient()
    return await theClient.deploy_chatbot_validate(req)

@app.route(route="chatbots/deploy/application", auth_level=func.AuthLevel.ANONYMOUS)
async def deploy_chatbot_full(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('deploy_chatbot_full executed...')
    theClient = AzureFunctionDeployerClient()
    return await theClient.deploy_chatbot_full(req)


@app.route(route="chatbots/deploy/infrastructure")
@app.durable_client_input(client_name="client")
async def terraform_http_start(req: func.HttpRequest, client: str) -> func.HttpResponse:
    logging.warning('Starting terraform deployment orchestration')
    try:
        deployment_parameter = json.loads(req.form.get("deployment_parameter"))
        
        deployment_params = {
            'subscription_id': deployment_parameter.get("subscription_id"),
            'location': deployment_parameter.get("location"),
            'resource_group_name': deployment_parameter.get("resource_group_name"),
            'app_insights_name': deployment_parameter.get("app_insights_name"),
            'storage_account_name': deployment_parameter.get("storage_account_name"),
            'tenant_id': deployment_parameter.get("tenant_id"),
            'client_id': deployment_parameter.get("client_id"),
            'client_secret': deployment_parameter.get("client_secret"),
            "working_dir": "./terraform/azureFunctionTemplate.tf",
            "status": TerraformStatus.PENDING
        }
        logging.warning("Deployment Params:")
        logging.warning(json.dumps(deployment_params))


        # Create durable orchestration client
        await asyncio.sleep(5)
        instance_id = await client.start_new(
            "terraform_orchestrator", 
            None, 
            deployment_params
        )
        
        return client.create_check_status_response(
            req, 
            instance_id,
        )

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            f"Internal server error: {str(e)}", 
            status_code=500
        )


@app.orchestration_trigger(context_name="context", orchestration="terraform_orchestrator")
def terraform_orchestrator(context: df.DurableOrchestrationContext) -> Generator[Dict[str, Any], Any, Dict[str, Any]]:
    deployment_params = context.get_input()
    logging.warning(context)
    
    retry_options = df.RetryOptions(
        first_retry_interval_in_milliseconds=3000,
        max_number_of_attempts=3
    )

    try:
        apply_result = yield context.call_activity_with_retry(
            "terraform_execute",
            retry_options,
            deployment_params
        )    
        logging.warning("terraform done")
        return apply_result

    except Exception as e:
        logging.error(f"Orchestration failed: {str(e)}")
        return {
            "success": False,
            "message": str(e),
            "status": TerraformStatus.FAILED
        }

@app.activity_trigger(input_name="params", activity="terraform_execute")
async def create_terraform_vars(params: dict) -> dict:
    logging.warning("Creating terraform variables file")
    try:
        tf = TerraformExecutor(variables=params)
        await tf.execute() 
        await asyncio.sleep(5)
        return {
            "success": True,
            "message": "Terraform completed successfully",
            "status": TerraformStatus.COMPLETE
        }
    except Exception as e:
        logging.error(f"Failed to create terraform variables: {str(e)}")
        return {
            "success": False,
            "message": str(e),
            "status": TerraformStatus.FAILED
        }