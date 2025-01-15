import asyncio
from typing import Any, AsyncGenerator, Dict, Generator
from dotenv import load_dotenv
from telegramClient import TelegramClient
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
# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Regular HTTP-triggered functions
@app.route(route="telegram")
async def process_telegram_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function "processTelegramMessage" processed a request.')
    theClient = TelegramClient()
    return await theClient._process_message(req)

@app.route(route="temp", auth_level=func.AuthLevel.ANONYMOUS)
def process_temp_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )

@app.route(route="chatbots/search", auth_level=func.AuthLevel.ANONYMOUS)
async def search_chatbots(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient._get_chatbots_by_sql(req)

@app.route(route="chatbots", auth_level=func.AuthLevel.ANONYMOUS)
async def get_chatbots(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python HTTP trigger function processed a request.')
    theClient = BackendClient()
    return await theClient._get_chatbots(req)

@app.route(route="chatbots/activate", auth_level=func.AuthLevel.ANONYMOUS)
async def activate_chatbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('activate_chatbot executed...')
    theClient = BackendClient()
    return await theClient._activate_chatbot(req)

@app.route(route="chatbots/deactivate", auth_level=func.AuthLevel.ANONYMOUS)
async def deactivate_chatbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('deactivate_chatbot executed...')
    theClient = BackendClient()
    return await theClient._deactivate_chatbot(req)

@app.route(route="chatbots/update", auth_level=func.AuthLevel.ANONYMOUS)
async def update_chatbot(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('update_chatbot executed...')
    theClient = BackendClient()
    return await theClient._update_chatbot(req)

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
            "working_dir": "./terraform",
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
        # 1. Create terraform.tfvars.json
        deployment_params["status"] = TerraformStatus.CREATING_VARS
        vars_result = yield context.call_activity_with_retry(
            "create_terraform_vars",
            retry_options,
            deployment_params
        )
        if not vars_result["success"]:
            return vars_result
        
        # 2. Initialize Terraform
        deployment_params["status"] = TerraformStatus.INITIALIZING
        init_result = yield context.call_activity_with_retry(
            "terraform_init",
            retry_options,
            deployment_params
        )
        if not init_result["success"]:
            return init_result
            
        # 3. Run Terraform Plan
        deployment_params["status"] = TerraformStatus.PLANNING
        plan_result = yield context.call_activity_with_retry(
            "terraform_plan",
            retry_options,
            deployment_params
        )
        if not plan_result["success"]:
            return plan_result
            
        # 4. Run Terraform Apply
        deployment_params["status"] = TerraformStatus.APPLYING
        apply_result = yield context.call_activity_with_retry(
            "terraform_apply",
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

@app.activity_trigger(input_name="params", activity="create_terraform_vars")
async def create_terraform_vars(params: dict) -> dict:
    logging.warning("Creating terraform variables file")
    try:
        tf = TerraformExecutor(params["working_dir"])
        variables = {
            "resource_group_name": params["resource_group_name"],
            "location": params["location"],
            "subscription_id": params["subscription_id"],
            "app_insights_name": params["app_insights_name"],
            "storage_account_name": params["storage_account_name"],
            "client_id": params["client_id"],
            "client_secret": params["client_secret"],
            "tenant_id": params["tenant_id"]
        }
        await tf.create_tfvars(variables)  # Added await
        await asyncio.sleep(5)
        return {
            "success": True,
            "message": "Variables file created successfully",
            "status": TerraformStatus.CREATING_VARS
        }
    except Exception as e:
        logging.error(f"Failed to create terraform variables: {str(e)}")
        return {
            "success": False,
            "message": str(e),
            "status": TerraformStatus.FAILED
        }

@app.activity_trigger(input_name="params", activity="terraform_init")
async def terraform_init(params: dict) -> dict:
    logging.warning("Initializing terraform")
    try:
        tf = TerraformExecutor(params["working_dir"])
        success, output = await tf.init()  # Added await
        await asyncio.sleep(5)
        return {
            "success": success,
            "message": output,
            "status": TerraformStatus.INITIALIZING if success else TerraformStatus.FAILED
        }
    except Exception as e:
        logging.error(f"Terraform init failed: {str(e)}")
        return {
            "success": False,
            "message": str(e),
            "status": TerraformStatus.FAILED
        }

@app.activity_trigger(input_name="params", activity="terraform_plan")
async def terraform_plan(params: dict) -> dict:
    logging.warning("Running terraform plan")
    try:
        tf = TerraformExecutor(params["working_dir"])
        success, output = await tf.plan()  # Added await
        await asyncio.sleep(5)
        return {
            "success": success,
            "message": output,
            "status": TerraformStatus.PLANNING if success else TerraformStatus.FAILED
        }
    except Exception as e:
        logging.error(f"Terraform plan failed: {str(e)}")
        return {
            "success": False,
            "message": str(e),
            "status": TerraformStatus.FAILED
        }

@app.activity_trigger(input_name="params", activity="terraform_apply")
async def terraform_apply(params: dict) -> dict:
    logging.warning("Running terraform apply")
    try:
        tf = TerraformExecutor(params["working_dir"])
        success, output = await tf.apply(auto_approve=True)  # Added await
        await asyncio.sleep(5)
        return {
            "success": success,
            "message": output,
            "status": TerraformStatus.COMPLETE if success else TerraformStatus.FAILED
        }
    except Exception as e:
        logging.error(f"Terraform apply failed: {str(e)}")
        return {
            "success": False,
            "message": str(e),
            "status": TerraformStatus.FAILED
        }