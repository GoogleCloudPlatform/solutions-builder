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
from typing import Optional
from typing_extensions import Annotated
from copier import run_copy
from .cli_utils import *
from .component import update_component

update_command = typer.Typer()

# Update a solution


@update_command.command()
def solution(solution_path: Annotated[Optional[str],
                                      typer.Argument()] = ".",
             template_path=None):
  """
  Update an existing solution folder.
  """
  if not solution_path:
    solution_path = "."

  validate_solution_folder(solution_path)

  if not os.path.exists(solution_path):
    raise FileNotFoundError(f"Solution folder {solution_path} does not exist.")

  confirm_msg = "This will update the current solution folder. Continue?"
  if solution_path != ".":
    confirm_msg = "This will update solution root folder at " \
        "'{solution_path}'. Continue?"
  confirm(confirm_msg)

  # Copy template_root to destination, excluding skaffold.yaml.
  orig_sb_yaml = read_yaml(f"{solution_path}/sb.yaml")

  if not template_path:
    current_dir = os.path.dirname(__file__)
    template_path = f"{current_dir}/../template_root"
    if not os.path.exists(template_path):
      raise FileNotFoundError(f"{template_path} does not exist.")

  worker = run_copy(template_path,
                    solution_path,
                    exclude=["skaffold.yaml", "sb.yaml"],
                    unsafe=True)
  answers = worker.answers.last

  # Restore some fields in sb.yaml.
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  sb_yaml["created_at"] = orig_sb_yaml["created_at"]
  sb_yaml["components"] = orig_sb_yaml["components"]
  write_yaml(f"{solution_path}/sb.yaml", sb_yaml)

  print_success(f"Complete. Solution folder updated at {solution_path}.\n")


@update_command.command()
def component(component_name,
              solution_path: Annotated[Optional[str],
                                       typer.Argument()] = ".",
              yes: Optional[bool] = False,
              answers=None):
  """
  Update an existing component folder.
  """
  update_component(component_name, solution_path, yes, answers)
