from datetime import datetime
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import ResourceNotFoundError, AzureError
from typing import Tuple, Dict, Any, Optional
from exceptions import ChatbotValidationError
import azure.functions as func
import requests
import asyncio
import copy
import os
import logging
import io
import zipfile
import mimetypes
import json
import base64
import ast
import uuid


async def _deploy_chatbot(req: func.HttpRequest) -> func.HttpResponse:

    '''
    TODO:
    First need to find out how to deploy without az login
    Then Need account for telegram support, external resource group
    '''
    try:
        uploaded_data = await _destrucuture_zip_folder(req=req)
        flag = await _validate_zip_folder(uploaded_data=uploaded_data)

        # Validate whether folder structure is fine, i.e Chatbot.py & main() & requirements.txt exists
        if flag:
            logging.warning("validation passed")
            azure_function_app = await _convert_to_azure_functions(uploaded_data)
            deployment_config = {
                "subscription_id": os.getenv("SUBSCRIPTION_ID"),
                "resource_group_name" : os.getenv("RESOURCE_GROUP_NAME"),
                "storage_account_name" : os.getenv("STORAGE_ACCOUNT_NAME"),
                "app_insights_name" : os.getenv("APP_INSIGHTS_NAME"),
                "location" : os.getenv("LOCATION", "southeastasia")
            }
            
            deployer = AzureFunctionDeployer(**deployment_config)
                    
            # Deploy function app with code
            chatbot_name = req.params.get('chatbot_name') # TODO: Add validation for the Name
            logging.warning(chatbot_name)
            result = await deployer.deploy_function_app(
                function_app_name=chatbot_name,
                files_dict=azure_function_app['files']
            )
            
            if result:
                name, unique_name, url = result
                return func.HttpResponse(
                    body=f"Successfully deployed {name} at {url}, You can test your function at: {url}/api/chatbot",
                    mimetype="text/plain",
                    status_code=200
                )
            else:
                logging.warning("Deployment failed")
                return func.HttpResponse(
                body="Deployment failed",
                mimetype="text/plain",
                status_code=500
            )

                
    except zipfile.BadZipFile:
        return func.HttpResponse(
            "Error: Invalid zip file",
            status_code=400
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )

def _is_text_file(filename: str) -> bool:
    """Basic check if a file might be text-based using common text extensions"""
    text_extensions = {
        '.txt', '.json', '.xml', '.html', '.css', '.js', '.jsx', 
        '.ts', '.tsx', '.md', '.yml', '.yaml', '.csv', '.log',
        '.py', '.java', '.c', '.cpp', '.h', '.sh', '.bat'
    }
    return filename.lower().endswith(tuple(text_extensions))

async def _destrucuture_zip_folder(req: func.HttpRequest) -> object:
    try:
        # Get the zip file from request body
        zip_data = req.get_body()
        
        # Create a BytesIO object from the zip data
        zip_buffer = io.BytesIO(zip_data)
        
        # Dictionary to store file contents
        processed_files = {}
        
        # Variable to store root directory name
        root_dir = None
        
        # Open and process the zip file
        with zipfile.ZipFile(zip_buffer) as zip_ref:
            # Get all file names
            all_files = zip_ref.namelist()
            
            # Find root directory name
            if all_files:
                first_path = all_files[0]
                # Get the first directory name
                root_dir = first_path.split('/')[0] if '/' in first_path else None
            
            # Process each file in the zip
            for file_name in all_files:
                with zip_ref.open(file_name) as file:
                    content = file.read()
                    
                    # Try to process as text if it looks like a text file
                    if _is_text_file(file_name):
                        try:
                            processed_files[file_name] = {
                                'content': content.decode('utf-8'),
                                'is_binary': False
                            }
                            continue
                        except UnicodeDecodeError:
                            # If text decoding fails, treat as binary
                            pass
                    
                    # Handle as binary file
                    processed_files[file_name] = {
                        'content': base64.b64encode(content).decode('utf-8'),
                        'is_binary': True
                    }
        
        # Prepare response
        response_data = {
            'status': 'success',
            'root_directory': root_dir,  # Added root directory name
            'file_count': len(processed_files),
            'files': {
                filename: {
                    'is_binary': info['is_binary'],
                    'mime_type': mimetypes.guess_type(filename)[0] or 'application/octet-stream',
                    'content': info['content']
                }
                for filename, info in processed_files.items()
            }
        }
        return response_data
    
    except zipfile.BadZipFile:
        return ValueError("BadZipFile detected, Error processing zipfile...")

async def _validate_zip_folder(uploaded_data: Dict[str, Any]) -> Tuple[bool, str]:
    try:
        files = uploaded_data.get('files', {})
        if not files:
            return False, "No files found in the uploaded data"
        required_files = ['test-python/requirements.txt', 'test-python/chatbot.py']
        for required_file in required_files:
            if required_file not in files:
                raise ChatbotValidationError(f"Missing required file: {required_file}")
            
            # Check if file is not empty directory
            if files[required_file].get('content', '') == '':
                raise ChatbotValidationError(f"Required file is empty: {required_file}")

        # Get chatbot.py content
        chatbot_content = files['test-python/chatbot.py']['content']
        
        # Parse Python code to check for main function
        try:
            tree = ast.parse(chatbot_content)
            
            # Look for main function definition
            main_function_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.AsyncFunctionDef) and node.name == 'main':
                    # Check function parameters
                    args = node.args
                    if len(args.args) != 1:
                        raise ChatbotValidationError("main function must have exactly one parameter")
                    
                    # Check parameter type annotation
                    if hasattr(args.args[0], 'annotation'):
                        if not isinstance(args.args[0].annotation, ast.Name) or args.args[0].annotation.id != 'str':
                            raise ChatbotValidationError("main function parameter must be annotated as 'str'")
                    
                    # Check return type annotation
                    if hasattr(node, 'returns'):
                        if not isinstance(node.returns, ast.Name) or node.returns.id != 'str':
                            raise ChatbotValidationError("main function must return 'str'")
                    
                    main_function_found = True
                    break
            
            if not main_function_found:
                raise ChatbotValidationError("main function not found in chatbot.py")

        except SyntaxError:
            raise ChatbotValidationError("Invalid Python syntax in chatbot.py")
        
        return True

    except Exception as e:
        raise ChatbotValidationError(f"Validation error: {str(e)}")

async def _convert_to_azure_functions(processed_data: dict) -> dict:
    """
    Converts processed files into Azure Functions structure by adding required files
    and organizing the content appropriately.
    
    Args:
        processed_files (dict): Dictionary containing processed file information
        
    Returns:
        dict: Updated files dictionary with Azure Functions structure
    """
    # Deep copy the processed files to avoid modifying the original
    azure_data = copy.deepcopy(processed_data)
    root_directory = azure_data['root_directory']
    
    # Add host.json configuration
    host_json_content = {
        "version": "2.0",
        "logging": {
            "applicationInsights": {
                "samplingSettings": {
                    "isEnabled": True,
                    "excludedTypes": "Request"
                }
            }
        },
        "extensionBundle": {
            "id": "Microsoft.Azure.Functions.ExtensionBundle",
            "version": "[3.*, 4.0.0)"
        }
    }
    
    azure_data['files'][f'{root_directory}/host.json'] = {
        'is_binary': False,
        'mime_type': 'application/json',
        'content': json.dumps(host_json_content, indent=2)
    }
    
    # Add function_app.py with basic imports and setup
    function_app_content = '''
from azure.functions import FunctionApp, HttpRequest, HttpResponse, AuthLevel
from chatbot import main
import json
import logging

app = FunctionApp(http_auth_level=AuthLevel.ANONYMOUS)

@app.route(route="chatbot", auth_level=AuthLevel.ANONYMOUS)
async def get_chatbot_response(req: HttpRequest) -> HttpResponse:
    try:
        logging.info('Processing get_chatbot_response')
        
        # Check if request has a body
        request_body = req.get_json()
        if not request_body or 'query' not in request_body:
            return HttpResponse(
                body=json.dumps({"error": "Missing 'query' in request body"}),
                mimetype="application/json",
                status_code=400
            )

        # Get query and process it
        query = request_body.get('query')
        response_body = await main(query)
        
        return HttpResponse(
            body=json.dumps(response_body),
            mimetype="application/json",
            status_code=200
        )
            
    except ValueError as ve:
        return HttpResponse(
            body=json.dumps({"error": "Invalid JSON in request body"}),
            mimetype="application/json",
            status_code=400
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return HttpResponse(
            body=json.dumps({"error": "Unknown error from processing get_chatbot_response"}),
            mimetype="application/json",
            status_code=500
        )
'''
    
    azure_data['files'][f'{root_directory}/function_app.py'] = {
        'is_binary': False,
        'mime_type': 'text/x-python',
        'content': function_app_content.strip()
    }
    
    # Add requirements.txt if it doesn't exist
    if f'{root_directory}/requirements.txt' not in azure_data['files']:
        requirements_content = '''
azure-functions
azure-functions-worker
'''
        azure_data['files'][f'{root_directory}/requirements.txt'] = {
            'is_binary': False,
            'mime_type': 'text/plain',
            'content': requirements_content.strip()
        }
    
    # Add .funcignore if it doesn't exist
    funcignore_content = '''
.git*
.vscode
local.settings.json
test
.venv
'''
    azure_data['files'][f'{root_directory}/.funcignore'] = {
        'is_binary': False,
        'mime_type': 'text/plain',
        'content': funcignore_content.strip()
    }
    
    # Add local.settings.json template
    local_settings_content = {
        "IsEncrypted": False,
        "Values": {
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "AzureWebJobsStorage": ""
        }
    }
    
    azure_data['files'][f'{root_directory}/local.settings.json'] = {
        'is_binary': False,
        'mime_type': 'application/json',
        'content': json.dumps(local_settings_content, indent=2)
    }
    azure_data['file_count'] = len(azure_data['files'])

    
    return {
        'status': 'success',
        'message': 'Successfully converted to Azure Functions structure',
        'root_directory': azure_data['root_directory'],
        'file_count': azure_data['file_count'],
        'files': azure_data['files']
    }

class AzureFunctionDeployer:
    def __init__(
        self,
        subscription_id: str,
        resource_group_name: str,
        storage_account_name: str,
        app_insights_name: str,
        location: str 
    ):
        self.credential = ClientSecretCredential(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            tenant_id=os.getenv("TENANT_ID")
            )
        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.storage_account_name = storage_account_name
        self.app_insights_name = app_insights_name
        self.location = location
        
        # Initialize Azure clients
        self.web_client = WebSiteManagementClient(
            credential=self.credential,
            subscription_id=self.subscription_id
        )
        self.resource_client = ResourceManagementClient(
            credential=self.credential,
            subscription_id=self.subscription_id
        )
        self.storage_client = StorageManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )
    
    def _create_in_memory_zip(self, files_dict: Dict[str, Any]) -> bytes:
        """Create an in-memory zip file from the files dictionary."""
        memory_zip = io.BytesIO()
        
        with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path, file_info in files_dict.items():
                # Skip directory entries and macOS system files
                if (file_info['is_binary'] and not file_info['content']) or '.DS_Store' in file_path:
                    continue
                
                # Remove the root directory from the path
                relative_path = file_path.split('/', 1)[1] if '/' in file_path else file_path
                
                # Write content to zip
                if file_info['is_binary']:
                    content = base64.b64decode(file_info['content'])
                else:
                    content = file_info['content'].encode('utf-8')
                    
                zf.writestr(relative_path, content)
        
        return memory_zip.getvalue()
    
    def generate_unique_name(self, base_name: str, max_length: int = 63) -> str:
        """
        Generate a unique function app name using base name and UUID.
        Azure Function names must be between 2-63 characters.
        """
        # Generate a short UUID (first 8 characters)
        short_uuid = str(uuid.uuid4())[:8]
        
        # Calculate maximum length for base name to ensure total length is within limits
        max_base_length = max_length - len(short_uuid) - 1  # -1 for the hyphen
        
        # Truncate base name if necessary
        if len(base_name) > max_base_length:
            base_name = base_name[:max_base_length]
            
        # Combine base name and UUID
        return f"{base_name}-{short_uuid}".lower()

    async def validate_existing_resources(self) -> bool:
        """Validate that all required resources exist."""
        try:
            # Check resource group
            self.resource_client.resource_groups.get(self.resource_group_name)
            
            # Check Application Insights
            app_insights = self.resource_client.resources.get_by_id(
                f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.Insights/components/{self.app_insights_name}"
            )
            
            return True
            
        except ResourceNotFoundError as e:
            logging.error(f"Resource validation failed: {str(e)}")
            return False

    async def deploy_function_app(
        self,
        function_app_name: str,
        files_dict: Dict[str, Any],
        python_version: str = "3.11",
        runtime_name: str = "python",
        runtime_version: str = "~4",
        use_uuid: bool = True
    ) -> Optional[str]:
        """
        Deploy an Azure Function App using existing resources.
        
        Args:
            function_app_name: Name of the function app to create
            python_version: Python version to use
            runtime_name: Runtime name (python)
            runtime_version: Runtime version (~4)
            use_uuid: Whether to append UUID to the base name
        Returns:
            str: Function app URL if successful, None otherwise
        """
        try:
            unique_function_app_name = self.generate_unique_name(function_app_name) if use_uuid else function_app_name

            storage_account_key = self.storage_client.storage_accounts.list_keys(
                self.resource_group_name,
                self.storage_account_name
            ).keys[0].value

            storage_connection_string = (
                f"DefaultEndpointsProtocol=https;"
                f"AccountName={self.storage_account_name};"
                f"AccountKey={storage_account_key};"
                "EndpointSuffix=core.windows.net"
            )

            # # Get existing app service plan
            # app_service_plan = self.web_client.app_service_plans.get(
            #     self.resource_group_name,
            #     self.app_service_plan_name
            # )

            # Create function app
            poller = self.web_client.web_apps.begin_create_or_update(
                resource_group_name=self.resource_group_name,
                name=unique_function_app_name,
                site_envelope={
                    "location": self.location,
                    "kind": "functionapp",
                    'sku': {
                            'name': 'Y1',
                            'tier': 'Dynamic'
                        },
                    "properties": {
                        "reserved": True,
                        "siteConfig": {
                            "linuxFxVersion": f"Python|{python_version}",
                            "appSettings": [
                                {
                                    "name": "FUNCTIONS_WORKER_RUNTIME",
                                    "value": runtime_name
                                },
                                {
                                    "name": "FUNCTIONS_EXTENSION_VERSION",
                                    "value": runtime_version
                                },
                                {
                                    "name": "AzureWebJobsStorage",
                                    "value": storage_connection_string
                                },
                                {
                                    "name": "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING",
                                    "value": storage_connection_string
                                },
                                {
                                    "name": "WEBSITE_CONTENTSHARE",
                                    "value": unique_function_app_name.lower()
                                },
                                {
                                    "name": "APPINSIGHTS_INSTRUMENTATIONKEY",
                                    "value": self.app_insights_name
                                },
                                {
                                    "name": "WEBSITE_RUN_FROM_PACKAGE",
                                    "value": "1"
                                }
                            ]
                        }
                    }
                }
            )
            
            function_app = poller.result()

            # Create zip file from the provided files
            zip_content = self._create_in_memory_zip(files_dict)

            # Get publishing credentials
            creds = self.web_client.web_apps.begin_list_publishing_credentials(
                self.resource_group_name,
                unique_function_app_name
            ).result()

            # Upload zip file using kudu zip deploy
            deploy_url = f"https://{unique_function_app_name}.scm.azurewebsites.net/api/zipdeploy"
            response = requests.post(
                    deploy_url,
                    headers={'Content-Type': 'application/zip'},
                    auth=(creds.publishing_user_name, creds.publishing_password),
                    data=zip_content
                )
                
            if response.status_code not in (200, 202):
                raise Exception(f"Deployment failed with status {response.status_code}: {response.text}")

            logging.info(f"Successfully deployed code to function app: {unique_function_app_name}")
                    
            return (function_app_name, unique_function_app_name, f"https://{function_app.default_host_name}")
            
        except Exception as e:
            logging.error(f"Error deploying function app: {str(e)}")
            return None
            