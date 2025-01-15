import logging
from typing import Dict, Any, List, Tuple
import subprocess
import json
import re
import os
import asyncio
import aiofiles

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
        logging.warning(f"Attempting to write tfvars to: {tfvars_path}")
        logging.warning(f"Current working directory: {os.getcwd()}")
        logging.warning(f"Directory exists: {os.path.exists(self.working_dir)}")
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