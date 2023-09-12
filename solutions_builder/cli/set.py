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
  root_st_yaml = read_yaml(f"{solution_path}/sb.yaml")
  old_project_id = root_st_yaml.get("project_id")
  old_project_number = root_st_yaml.get("project_number")
  assert old_project_id, "project_id does not exist in sb.yaml"

  confirm(
      f"This will replace all project-id '{old_project_id}' to '{new_project_id}' in folder '{solution_path}'. "
      + "Continue?",
      skip=yes)

  # Update Root sb.yaml
  new_project_number = int(get_project_number(new_project_id))
  assert new_project_number, "Unable to receive project number for project '{new_project_id}'"

  root_st_yaml["project_id"] = new_project_id
  root_st_yaml["project_number"] = new_project_number
  write_yaml(f"{solution_path}/sb.yaml", root_st_yaml)

  # Update copier answers
  copier_yaml = read_yaml(f"{solution_path}/.copier-answers.yml")
  copier_yaml["project_id"] = new_project_id
  copier_yaml["project_number"] = int(get_project_number(new_project_id))
  write_yaml(f"{solution_path}/.copier-answers.yml", copier_yaml)

  file_set = set()
  # Adding includes.
  for pattern in INCLUDE_PATTERNS:
    file_list = pathlib.Path(solution_path).rglob(f"{pattern}")
    file_set.update(set([str(x) for x in file_list]))

  # Removing excludes.
  for pattern in EXCLUDE_PATTERNS:
    file_list = pathlib.Path(solution_path).rglob(f"{pattern}")
    file_set = file_set - set([str(x) for x in file_list])

  for filename in list(file_set):
    with open(filename, "r") as file:
      filedata = file.read()
      # Replace project_id
      filedata = re.sub(old_project_id, new_project_id, filedata)
      # Replace project_number
      if old_project_number and new_project_number:
        filedata = re.sub(str(old_project_number), str(new_project_number), filedata)

    # Write back to the original file.
    with open(filename, "w") as file:
      file.write(filedata)

  print(
      f"\nReplaced project_id from '{old_project_id}' to '{new_project_id}'.")
  print(
      f"Replaced project_number from '{old_project_number}' to '{new_project_number}'.")
