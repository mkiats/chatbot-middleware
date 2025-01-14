from typing import Dict, Any, List, Tuple
import subprocess
import json
import re
import os
import asyncio
import aiofiles

async def deploy_azure_via_terraform(
   resource_group_name: str,
   location: str,
   subscription_id: str,
   app_insights_name: str,
   storage_account_name: str,
   client_id: str,
   client_secret: str,
   tenant_id: str,
   working_dir: str,
   auto_approve: bool = True
) -> tuple[bool, str]:
   """
   Deploy Azure infrastructure using Terraform
   
   Args:
       resource_group_name: Name of the resource group
       location: Azure region location
       subscription_id: Azure subscription ID
       app_insights_name: Name of Application Insights instance
       storage_account_name: Name of the storage account
       client_id: Azure service principal client ID
       client_secret: Azure service principal client secret
       tenant_id: Azure tenant ID
       working_dir: Directory containing Terraform configuration
       auto_approve: Whether to skip interactive approval
       
   Returns:
       Tuple of (success: bool, message: str)
   """
   try:
       # Initialize Terraform executor
       tf = TerraformExecutor(working_dir)
       
       # Create variables file
       variables = {
           "resource_group_name": resource_group_name,
           "location": location,
           "subscription_id": subscription_id,
           "app_insights_name": app_insights_name,
           "storage_account_name": storage_account_name,
           "client_id": client_id,
           "client_secret": client_secret,
           "tenant_id": tenant_id
       }
       await tf.create_tfvars(variables)
       
       # Initialize Terraform
       success, output = await tf.init()
       if not success:
           return False, f"Terraform init failed: {output}"
       
       # Run plan
       success, output = await tf.plan()
       if not success:
           return False, f"Terraform plan failed: {output}"
       
       # Apply configuration
       success, output = await tf.apply(auto_approve)
       if not success:
           return False, f"Terraform apply failed: {output}"
       
       return True, "Infrastructure deployed successfully"
       
   except Exception as e:
       return False, f"Deployment failed: {str(e)}"

class TerraformExecutor:
   def __init__(self, working_dir: str):
       self.working_dir = working_dir

   async def _run_command(self, command: list) -> tuple[int, str, str]:
       """
       Run a terraform command and return the exit code, stdout, and stderr
       """
       process = await asyncio.create_subprocess_exec(
           *command,
           stdout=asyncio.subprocess.PIPE,
           stderr=asyncio.subprocess.PIPE,
           cwd=self.working_dir
       )
       stdout, stderr = await process.communicate()
       return process.returncode, stdout.decode(), stderr.decode()

   async def create_tfvars(self, variables: Dict[str, Any]) -> None:
       """
       Create terraform.tfvars.json file from variables
       """
       tfvars_path = os.path.join(self.working_dir, "terraform.tfvars.json")
       async with aiofiles.open(tfvars_path, 'w') as f:
           await f.write(json.dumps(variables, indent=2))

   async def init(self) -> tuple[bool, str]:
       """
       Run terraform init
       """
       exit_code, stdout, stderr = await self._run_command(["terraform", "init"])
       return exit_code == 0, stderr if exit_code != 0 else stdout

   async def plan(self) -> tuple[bool, str]:
       """
       Run terraform plan
       """
       exit_code, stdout, stderr = await self._run_command(["terraform", "plan"])
       return exit_code == 0, stderr if exit_code != 0 else stdout

   async def apply(self, auto_approve: bool = False) -> tuple[bool, str]:
       """
       Run terraform apply
       """
       command = ["terraform", "apply"]
       if auto_approve:
           command.append("-auto-approve")
       
       exit_code, stdout, stderr = await self._run_command(command)
       return exit_code == 0, stderr if exit_code != 0 else stdout

   async def destroy(self, auto_approve: bool = False) -> tuple[bool, str]:
       """
       Run terraform destroy
       """
       command = ["terraform", "destroy"]
       if auto_approve:
           command.append("-auto-approve")
       
       exit_code, stdout, stderr = await self._run_command(command)
       return exit_code == 0, stderr if exit_code != 0 else stdout