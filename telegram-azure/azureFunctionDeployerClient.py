from azure.identity import ClientSecretCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from typing import Dict, Any, List, Optional, Tuple
from exceptions import DeploymentException
from entities import Chatbot, ChatbotStatus
from terraformClient import deploy_azure_via_terraform
from cosmos import CosmosDB
import azure.functions as func
import requests
import copy
import os
import re
import logging
import io
import zipfile
import mimetypes
import json
import base64
import ast
import uuid


class AzureFunctionDeployerClient:
    def __init__(self):
        self.name = ""
        self.version = ""
        self.function_app_name = ""
        self.endpoint = ""
        self.description = "Some description"
        self.developer_id = "123123123"
        self.telegram_support = True
        self.deployment_type = None
        self.subscription_id = None
        self.resource_group_name = None
        self.storage_account_name = None
        self.app_insights_name = None
        self.location = None

        self.credential = None
        self.web_client = None
        self.resource_client = None
        self.storage_client = None

    async def deploy_chatbot_validate(self, req: func.HttpRequest) -> func.HttpResponse:
        try:
            files = req.files["chatbot_file"]
            if not files:
                raise DeploymentException(message="No files uploaded", deployment_stage="Initial")
            uploaded_data = await self._destrucuture_zip_folder(files)
            logging.warning("Zip folder destructured...")
            validated_data = await self._validate_zip_folder(uploaded_data=uploaded_data)
            logging.warning("Zip folder validated...")
            await self._get_deployment_parameters(req)
            logging.warning("Deployment parameters retrieved...")
            response_body = {
                "validation": True,
                "error_message": ""
            }
            return func.HttpResponse(
                body=json.dumps(response_body),
                mimetype="application/json",
                status_code=200
                )
        except Exception as e:
            response_body = {
                "validation": False,
                "error_message": str(e)
            }
            return func.HttpResponse(
                body=json.dumps(response_body),
                mimetype="application/json",
                status_code=500
                )
                
            
        

    async def deploy_chatbot_full(self, req: func.HttpRequest) -> func.HttpResponse:

        try:
            files = req.files["chatbot_file"]
            if not files:
                raise DeploymentException(message="No files uploaded", deployment_stage="Initial")
            uploaded_data = await self._destrucuture_zip_folder(files)
            logging.warning("Zip folder destructured...")
            validated_data = await self._validate_zip_folder(uploaded_data=uploaded_data)
            logging.warning("Zip folder validated...")

            if validated_data:
                function_app_files = await self._create_required_azure_files(validated_data)
                zipped_function_app_files = await self._create_in_memory_zip(function_app_files)
                await self._get_deployment_parameters(req)
                self.function_app_name = await self._generate_unique_name(self.name)

                # Deploy function app with code
                result = await self._deploy_function_app(
                    function_app_name=self.function_app_name,
                    function_app_files=zipped_function_app_files
                )                
                if result:
                    self.endpoint = f"{result}/api/chat/query"
                    await self._register_new_chatbot()
                    response = func.HttpResponse(
                            body=json.dumps({
                                "message": f"Successfully deployed {self.name}, You can test your function at: {self.endpoint}",
                                "endpoint": self.endpoint
                            }),
                            mimetype="application/json",
                            status_code=200
                        )
                    # Add CORS headers
                    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
                    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
                    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
                    return response
                else:
                    logging.warning("Deployment failed")
                    return func.HttpResponse(
                        body="Deployment failed",
                        mimetype="text/plain",
                        status_code=500
                    )

        except Exception as e:
            logging.error(str(e))
            return func.HttpResponse(
                body=str(e),
                status_code=500,
                mimetype="text/plain"
            )

    async def _destrucuture_zip_folder(self, files: Any) -> object:

        def _is_text_file(filename: str) -> bool:
            """Basic check if a file might be text-based using common text extensions"""
            text_extensions = {
                '.txt', '.json', '.xml', '.html', '.css', '.js', '.jsx', 
                '.ts', '.tsx', '.md', '.yml', '.yaml', '.csv', '.log',
                '.py', '.java', '.c', '.cpp', '.h', '.sh', '.bat'
            }
            return filename.lower().endswith(tuple(text_extensions))

        try:
            # Get the zip file from request body
            # zip_data = req.get_body()
            # files = await req.files.get('file')  # 'file' is the form field name
            if not files:
                raise DeploymentException(message="No file found in request", deployment_stage="DestructureZipFolder")

            # Read the file into bytes
            zip_data = files.stream.read()
            zip_buffer = io.BytesIO(zip_data)
            processed_files = {}
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
                'root_directory': root_dir,
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
            raise DeploymentException(message="Bad zip file detected", deployment_stage="DestructureZipFolder") 
        
        except Exception as e:
            raise DeploymentException(message="Unknown error", deployment_stage="DestructureZipFolder")

    async def _validate_zip_folder(self, uploaded_data: Dict[str, Any]) -> object:
        try:
            files = uploaded_data.get('files', {})
            if not files:
                return None
            
            # Look for required files
            required_files = [f"{uploaded_data.get('root_directory')}/requirements.txt", f"{uploaded_data.get('root_directory')}/chatbot.py"]
            for required_file in required_files:
                if required_file not in files:
                    raise DeploymentException(message=f"Missing required file: {required_file}", deployment_stage="ValidateZipFolder")
                
                # Check if file is not empty directory
                if files[required_file].get('content', '') == '':
                    raise DeploymentException(message=f"Required file is empty: {required_file}", deployment_stage="ValidateZipFolder")

            # Get chatbot.py content
            chatbot_content = files[f"{uploaded_data.get('root_directory')}/chatbot.py"]['content']
            

            try:
                tree = ast.parse(chatbot_content)            
                # Look for async main function definition
                main_function_found = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.AsyncFunctionDef) and node.name == 'main':
                        # Check function parameters
                        args = node.args
                        if len(args.args) != 1:
                            raise DeploymentException(message="main function must have exactly one parameter", deployment_stage="ValidateZipFolder")
                        
                        # Check parameter type annotation
                        if hasattr(args.args[0], 'annotation'):
                            if not isinstance(args.args[0].annotation, ast.Name) or args.args[0].annotation.id != 'str':
                                raise DeploymentException(message="main function parameter must be annotated as 'str'", deployment_stage="ValidateZipFolder")
                        
                        # Check return type annotation
                        if hasattr(node, 'returns'):
                            if not isinstance(node.returns, ast.Name) or node.returns.id != 'str':
                                raise DeploymentException(message="main function must return 'str'", deployment_stage="ValidateZipFolder")
                        
                        main_function_found = True
                        break
                
                if not main_function_found:
                    raise DeploymentException(message="main function not found in chatbot.py", deployment_stage="ValidateZipFolder")

            except SyntaxError:
                raise DeploymentException(message="Invalid Python syntax in chatbot.py", deployment_stage="ValidateZipFolder")
            
            return uploaded_data

        except Exception as e:
            raise DeploymentException(message=f"Unknown error", deployment_stage="ValidateZipFolder")

    async def _create_required_azure_files(self, processed_data: dict) -> dict:
        """
        Converts processed files into Azure Functions structure by adding required files
        and organizing the content appropriately.
        
        Args:
            processed_files (dict): Dictionary containing processed file information
            
        Returns:
            dict: Updated files dictionary with Azure Functions structure
        """
        try:
                
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

@app.route(route="chat/query", auth_level=AuthLevel.ANONYMOUS)
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
        except Exception as e:
            raise DeploymentException(message=f"Unknown error", deployment_stage="CreateRequiredAzureFiles")

    async def _create_in_memory_zip(self, app_files: Dict[str, Any]) -> bytes:
        try:

            """Create an in-memory zip file from the files dictionary."""
            memory_zip = io.BytesIO()
            
            with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path, file_info in app_files['files'].items():
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
        except Exception as e:
            raise DeploymentException(message="Unknown error", deployment_stage="CreateZipFolder")

    async def _get_deployment_parameters(self, req: func.HttpRequest) -> None:
        """
        Process deployment parameters from the request and set up configuration.
        Supports managed, custom, and terraform deployment types.
        """
        try:
            # Extract and parse deployment parameters
            deployment_parameter = json.loads(req.form.get("deployment_parameter"))
            logging.warning(json.dumps(deployment_parameter))
            
            # Set basic parameters
            self.name = deployment_parameter.get("name")
            self.version = deployment_parameter.get("version")
            self.description = deployment_parameter.get("description")
            self.status = ChatbotStatus(deployment_parameter.get("status"))
            self.developer_id = deployment_parameter.get("developer_id")
            self.telegram_support = deployment_parameter.get("telegram_support")
            
            # Set deployment type with default to managed
            self.deployment_type = deployment_parameter.get("deployment_type", "managed")
            
            # Handle managed deployment
            if self.deployment_type == "managed":
                self.subscription_id = os.getenv("SUBSCRIPTION_ID")
                self.resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
                self.storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME")
                self.app_insights_name = os.getenv("APP_INSIGHTS_NAME")
                self.location = os.getenv("LOCATION", "southeastasia")
                self.credential = ClientSecretCredential(
                    client_id=os.getenv("CLIENT_ID"),
                    client_secret=os.getenv("CLIENT_SECRET"),
                    tenant_id=os.getenv("TENANT_ID")
                )

            # Handle custom or terraform deployment
            elif self.deployment_type in ("custom", "terraform"):

                # Set configuration parameters
                self.subscription_id = deployment_parameter.get('subscription_id')
                self.resource_group_name = deployment_parameter.get('resource_group_name')
                self.storage_account_name = deployment_parameter.get('storage_account_name')
                self.app_insights_name = deployment_parameter.get('app_insights_name')
                self.location = deployment_parameter.get("location")
                self.credential = ClientSecretCredential(
                    client_id=deployment_parameter.get('client_id'),
                    client_secret=deployment_parameter.get('client_secret'),
                    tenant_id=deployment_parameter.get('tenant_id')
                )
            else:
                raise DeploymentException("Invalid deployment type", "GetDeploymentParameter")

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
                subscription_id=self.subscription_id
            )
        except DeploymentException as deploymentException:
            raise deploymentException
        
        except Exception as e:
            raise DeploymentException(message="Unknown error, {e}", deployment_stage="GetDeploymentParameter")
    
    async def _generate_unique_name(self, base_name: str, max_length: int = 63) -> str:
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

    async def _deploy_function_app(
        self,
        function_app_name: str,
        function_app_files: bytes,
        python_version: str = "3.11",
        runtime_name: str = "python",
        runtime_version: str = "~4",
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
                name=function_app_name,
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
                                    "value": function_app_name.lower()
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

            # Get publishing credentials
            creds = self.web_client.web_apps.begin_list_publishing_credentials(
                self.resource_group_name,
                function_app_name
            ).result()

            # Upload zip file using kudu zip deploy
            deploy_url = f"https://{function_app_name}.scm.azurewebsites.net/api/zipdeploy"
            response = requests.post(
                    deploy_url,
                    headers={'Content-Type': 'application/zip'},
                    auth=(creds.publishing_user_name, creds.publishing_password),
                    data=function_app_files
                )
                
            if response.status_code not in (200, 202):
                raise Exception(f"Deployment failed with status {response.status_code}: {response.text}")

            logging.info(f"Successfully deployed code to function app: {function_app_name}")
                    
            return f"https://{function_app.default_host_name}"
            
        except Exception as e:
            logging.error(f"Error deploying function app: {e}")
            raise DeploymentException(message="Error deploying function app: {str(e)}", deployment_stage="DeployFunctionApp")

    async def _register_new_chatbot(self):
        try:
            newChatbot = Chatbot(
                name=self.name,
                version=self.version,
                endpoint=self.endpoint,
                description=self.description,
                status=self.status,
                developer_id=self.developer_id,
                telegram_support=self.telegram_support,
                deployment_resource={
                    'deployment_type': self.deployment_type,
                    'resource_group_name': self.resource_group_name,
                    'location': self.location,
                    'subscription_id': self.subscription_id,
                    'app_insights_name': self.app_insights_name,
                    'storage_account_name': self.storage_account_name
                }
            )
            newChatbot.validate()
            db = CosmosDB()
            await db.initialize()
            db.chatbot_container.upsert_item(body=newChatbot.to_dict())
        except Exception as e:
            raise DeploymentException(message=f"Unknown error {e}", deployment_stage="RegisterNewChatbot")

    def validate_azure_config(self, config: Dict[str, Any], terraform_deployment: bool = False) -> Tuple[bool, List[str], Dict[str, Any]]:

        """
        Validates and prepares the Azure infrastructure configuration.
        
        Args:
            config: Dictionary containing configuration parameters
            
        Returns:
            Tuple containing:
                - bool: True if valid, False if invalid
                - List[str]: List of error messages (empty if valid)
                - Dict[str, Any]: Processed configuration with defaults (empty if invalid)
        """
        errors = []
        
        # Required fields check

        required_fields = {
            'subscription_id': str,
            'location': str,
            'resource_group_name': str,
            'app_insights_name': str,
            'storage_account_name': str,
            'tenant_id': str,
            'client_id': str,
            'client_secret': str,
        }
        if terraform_deployment:
            required_fields = {
                **required_fields,
                'working_dir': str
            }
        
        
        # Check missing or invalid type fields
        for field, expected_type in required_fields.items():
            if field not in config:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(config[field], expected_type):
                errors.append(f"Invalid type for {field}: expected {expected_type.__name__}, got {type(config[field]).__name__}")

        # Location validation (optional with default)
        if 'location' in config:
            if not isinstance(config['location'], str):
                errors.append("Invalid type for location: expected str")
            elif not config['location']:
                errors.append("Location cannot be empty if provided")

        # Working directory validation
        if terraform_deployment and 'working_dir' in config and isinstance(config['working_dir'], str):
            if not os.path.exists(config['working_dir']):
                errors.append(f"Working directory does not exist: {config['working_dir']}")
            elif not os.path.isdir(config['working_dir']):
                errors.append(f"Working directory path is not a directory: {config['working_dir']}")

        # Resource naming conventions
        naming_rules = {
            'resource_group_name': (r'^[a-zA-Z0-9-_]{1,90}$', 
                                "Resource group name must be 1-90 characters long and can only contain alphanumeric characters, hyphens, and underscores"),
            'storage_account_name': (r'^[a-z0-9]{3,24}$',
                                "Storage account name must be 3-24 characters long and can only contain lowercase letters and numbers"),
            'app_insights_name': (r'^[a-zA-Z0-9-]{1,260}$',
                                "Application Insights name must be 1-260 characters long and can only contain alphanumeric characters and hyphens")
        }

        for field, (pattern, error_msg) in naming_rules.items():
            if field in config and isinstance(config[field], str):
                if not re.match(pattern, config[field]):
                    errors.append(error_msg)

        # GUID format validation
        guid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        guid_fields = ['subscription_id', 'client_id', 'tenant_id']
        
        for field in guid_fields:
            if field in config and isinstance(config[field], str):
                if not re.match(guid_pattern, config[field].lower()):
                    errors.append(f"{field} must be a valid GUID")

        # If there are errors, return early
        if errors:
            return False, errors, {}

        # Prepare processed config with defaults
        processed_config = config.copy()
        if 'location' not in processed_config:
            processed_config['location'] = 'southeastasia'
        
        return True, [], processed_config
    

    # async def validate_existing_resources(self) -> bool:
    #     """Validate that all required resources exist."""
    #     try:
    #         # Check resource group
    #         self.resource_client.resource_groups.get(self.resource_group_name)
            
    #         # Check Application Insights
    #         app_insights = self.resource_client.resources.get_by_id(
    #             f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.Insights/components/{self.app_insights_name}"
    #         )
            
    #         return True
            
    #     except ResourceNotFoundError as e:
    #         logging.error(f"Resource validation failed: {str(e)}")
    #         return False