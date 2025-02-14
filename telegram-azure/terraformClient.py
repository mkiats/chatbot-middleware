import logging
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from azure.storage.fileshare import ShareServiceClient, ShareClient, ShareDirectoryClient
from typing import Dict, Any, List, Tuple
from uuid import uuid4
import subprocess
import json
import re
import os
import asyncio
import aiofiles
from time import sleep


class TerraformExecutor:
    def __init__(self, variables: Dict[str, Any]):
        credential = ClientSecretCredential(
            client_id=os.getenv("MKIATS_ID"),
            client_secret=os.getenv("MKIATS_SECRET"),
            tenant_id=os.getenv("TENANT_ID"),
        )
        # Blob Storage: For retrieval of Terraform templates
        blob_account_url = os.environ.get("BLOB_STORAGE_ACCOUNT_URI")
        self.blob_service_client = BlobServiceClient(
            account_url=blob_account_url, credential=credential
        )
        self.blob_container_name = self.blob_service_client.get_container_client(container="terraform")

        # File share: For writable file directory
        # file_share_account_url = os.environ.get("FILE_SHARE_STORAGE_ACCOUNT_URI")
        # logging.warning(f"file_share_account_url: {file_share_account_url}")
        self.unique_file_share_directory = f"terraform_{str(uuid4())[:8]}"
        # self.share_service_client: ShareServiceClient = ShareServiceClient(account_url=file_share_account_url, credential=credential)
        # self.share_client: ShareClient = self.share_service_client.get_share_client(share="terraform")
        # self.share_directory_client: ShareDirectoryClient = self.share_client.create_directory(directory_name=file_share_account_url)

        # Client input
        self.variables = variables
        logging.warning(f"Current working directory: {os.getcwd()}")
        sleep(2)
        logging.warning(f"Listing directories: {os.listdir()}")
        sleep(2)
        logging.warning(f"Unique directory: {self.unique_file_share_directory}")
        sleep(2)
        if not os.path.exists(self.unique_file_share_directory):
            os.mkdir(f"./{self.unique_file_share_directory}")
        logging.warning(f"Listing directories: {os.listdir()}")
        logging.warning(f"Directory exists: {os.path.exists(self.unique_file_share_directory)}")




    async def execute(
        self,
        operation: str = "apply",
        auto_approve: bool = False,
    ) -> tuple[bool, str]:
        """
        Execute Terraform operations in sequence. This function orchestrates the entire Terraform workflow.

        Args:
            variables: Dictionary of terraform variables to be used
            operation: The terraform operation to perform after init/plan ("apply" or "destroy")
            auto_approve: Whether to automatically approve the operation without confirmation

        Returns:
            tuple[bool, str]: Success status and output/error message
        """
        logging.warning(f"Starting Terraform execution in {self.unique_file_share_directory}")
        sleep(5)
        try:
            # Step 1: Create tfvars file
            await self.create_tfvars(self.variables)
            logging.warning("Successfully created tfvars file")
            sleep(5)

            # Step 2: Initialize Terraform
            success, output = await self.init()
            if not success:
                logging.error(f"Terraform init failed: {output}")
                return False, f"Init failed: {output}"
            logging.warning("Terraform init completed successfully")
            sleep(5)

            # Step 3: Run Terraform plan
            success, output = await self.plan()
            if not success:
                logging.error(f"Terraform plan failed: {output}")
                return False, f"Plan failed: {output}"
            logging.warning("Terraform plan completed successfully")
            sleep(5)

            # Step 4: Run the specified operation (apply or destroy)
            if operation.lower() == "apply":
                success, output = await self.apply(auto_approve)
            elif operation.lower() == "destroy":
                success, output = await self.destroy(auto_approve)
            else:
                return False, f"Unsupported operation: {operation}"
            sleep(5)

            if not success:
                logging.error(f"Terraform {operation} failed: {output}")
                return False, f"{operation} failed: {output}"

            logging.warning(f"Terraform {operation} completed successfully")
            return True, output

        except Exception as e:
            error_msg = f"Unexpected error during Terraform execution: {str(e)}"
            logging.exception(error_msg)
            return False, error_msg

    async def _run_command(self, command: list) -> tuple[int, str, str]:
        """
        Run a terraform command and return the exit code, stdout, and stderr
        """
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.unique_file_share_directory,
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()

    async def create_tfvars(self, variables: Dict[str, Any]) -> None:
        """
        Create terraform.tfvars.json file from variables
        """
        # os.makedirs(self.unique_file_share_directory, exist_ok=True)
        tfvars_path = os.path.join(self.unique_file_share_directory, "terraform.tfvars.json")
        logging.warning(f"Attempting to write tfvars to: {tfvars_path}")

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
