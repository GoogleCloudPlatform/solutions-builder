"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import typer
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from .cli_utils import *

tool_app = typer.Typer()


@tool_app.command()
def project_number(working_dir: str = "."):
  project_id = typer.prompt("What's your GCP Project ID?")
  command = f"gcloud projects describe {project_id} --format='value(projectNumber)'"
  print("Executing the command below:")
  print(command)

  output = exec_output(command, working_dir=working_dir)
  print_highlight(output)
