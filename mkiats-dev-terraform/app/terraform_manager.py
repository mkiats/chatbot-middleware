import os
import json
import shutil
import logging
import asyncio
import aiofiles
from typing import Dict, Any, Tuple
from pathlib import Path


class TerraformManager:
    def __init__(self, template_dir: str):
        self.template_dir = template_dir
        self.temp_dir = None

    async def setup_workspace(self) -> None:
        """Create temporary workspace and copy template files"""
        # Create a temporary directory with timestamp
        self.temp_dir = os.path.join(
            "/tmp", f"terraform_{int(asyncio.get_event_loop().time() * 1000)}"
        )
        os.makedirs(self.temp_dir, exist_ok=True)
        logging.info(f'terraform template dir: {self.template_dir}')

        # Copy template files to temp directory
        try:
            for item in os.listdir(self.template_dir):
                source = os.path.join(self.template_dir, item)
                destination = os.path.join(self.temp_dir, item)
                if os.path.isfile(source):
                    shutil.copy2(source, destination)
                else:
                    shutil.copytree(source, destination)
            logging.info(
                f"Template files copied to temporary workspace: {self.temp_dir}"
            )
        except Exception as e:
            logging.error(f"Failed to copy template files: {str(e)}")
            await self.cleanup()
            raise

    async def _run_command(self, command: list) -> Tuple[int, str, str]:
        """Run a terraform command and return the exit code, stdout, and stderr"""
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.temp_dir,
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()

    # Create terraform variables: terraform.tfvars.json
    async def create_tfvars(self, variables: Dict[str, Any]) -> None:
        """Create terraform.tfvars.json file from variables"""
        tfvars_path = os.path.join(self.temp_dir, "terraform.tfvars.json")
        logging.info(f"Writing tfvars to: {tfvars_path}")

        async with aiofiles.open(tfvars_path, "w") as f:
            await f.write(json.dumps(variables, indent=2))

    async def init(self) -> Tuple[bool, str]:
        """Run terraform init"""
        logging.info(f"Running Terraform init")

        exit_code, stdout, stderr = await self._run_command(["terraform", "init"])
        return exit_code == 0, stderr if exit_code != 0 else stdout

    async def plan(self) -> Tuple[bool, str]:
        """Run terraform plan"""
        logging.info(f"Running Terraform plan")

        exit_code, stdout, stderr = await self._run_command(["terraform", "plan"])
        return exit_code == 0, stderr if exit_code != 0 else stdout

    async def apply(self, auto_approve: bool = True) -> Tuple[bool, str]:
        """Run terraform apply"""
        logging.info(f"Running Terraform apply")

        command = ["terraform", "apply"]
        if auto_approve:
            command.append("-auto-approve")

        exit_code, stdout, stderr = await self._run_command(command)
        return exit_code == 0, stderr if exit_code != 0 else stdout

    async def destroy(self, auto_approve: bool = False) -> Tuple[bool, str]:
        """Run terraform destroy"""
        logging.info(f"Running Terraform destroy")

        command = ["terraform", "destroy"]
        if auto_approve:
            command.append("-auto-approve")

        exit_code, stdout, stderr = await self._run_command(command)
        return exit_code == 0, stderr if exit_code != 0 else stdout

    async def cleanup(self) -> None:
        """Clean up temporary workspace"""
        logging.info(f"Running Terraform cleanup")

        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logging.info(f"Cleaned up temporary workspace: {self.temp_dir}")
            except Exception as e:
                logging.error(f"Failed to cleanup workspace: {str(e)}")
