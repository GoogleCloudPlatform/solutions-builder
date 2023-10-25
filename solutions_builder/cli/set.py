"""
Copyright 2023 Google LLC

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
import glob
import pathlib
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from .cli_utils import *
from .vars import set_var

set_app = typer.Typer()

INCLUDE_PATTERNS = [
    "*.yaml", "*.yml", "*.env", "*.tfvars", "*.tf", "*.sh", "*.md"
]
EXCLUDE_PATTERNS = ["**/.terraform/**/*.*", "**/node_modules/**/*.*"]


@set_app.command()
def project_id(
    new_project_id,
    solution_path: Annotated[Optional[str], typer.Argument()] = ".",
    yes: Optional[bool] = False,
):
  validate_solution_folder(solution_path)
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = sb_yaml.get("global_variables", {})

  old_project_id = global_variables.get("project_id")
  old_project_number = global_variables.get("project_number")
  assert old_project_id, "project_id does not exist in sb.yaml"

  confirm(
      f"This will replace all project-id '{old_project_id}' to '{new_project_id}' in folder '{solution_path}'. "
      + "Continue?",
      skip=yes)

  # Update Root sb.yaml
  new_project_number = int(get_project_number(new_project_id))
  assert new_project_number, "Unable to receive project number for project '{new_project_id}'"

  global_variables["project_id"] = new_project_id
  global_variables["project_number"] = new_project_number
  sb_yaml["global_variables"] = global_variables
  write_yaml(f"{solution_path}/sb.yaml", sb_yaml)

  # Update copier answers
  copier_yaml = read_yaml(f"{solution_path}/.copier-answers.yml")
  copier_yaml["project_id"] = new_project_id
  copier_yaml["project_number"] = int(get_project_number(new_project_id))
  write_yaml(f"{solution_path}/.copier-answers.yml", copier_yaml)

  set_var("project_id", new_project_id)
  set_var("project_number", new_project_number)

  print(
      f"\nReplaced project_id from '{old_project_id}' to '{new_project_id}'.")
  print(
      f"Replaced project_number from '{old_project_number}' to '{new_project_number}'.\n")
