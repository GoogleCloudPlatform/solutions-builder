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
import glob
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from .cli_utils import *

set_app = typer.Typer()

FILE_EXTENSIONS = ["yaml", "env", "tfvars", "sh", "md"]


@set_app.command()
def project_id(
    new_project_id,
    solution_path: Annotated[Optional[str], typer.Argument()] = ".",
    yes: Optional[bool] = False,
):
  validate_solution_folder(solution_path)
  root_st_yaml = read_yaml(f"{solution_path}/st.yaml")
  old_project_id = root_st_yaml.get("project_id")
  assert old_project_id, "project_id does not exist in st.yaml"

  confirm(
      f"This will replace all project-id '{old_project_id}' to '{new_project_id}' in folder '{solution_path}'. "
      + "Continue?",
      skip=yes)

  root_st_yaml["project_id"] = new_project_id
  root_st_yaml["project_number"] = get_project_number(new_project_id)
  write_yaml(f"{solution_path}/st.yaml", root_st_yaml)

  file_set = set()
  for filetype in FILE_EXTENSIONS:
    file_set.update(
        set(glob.glob(solution_path + f"/**/*.{filetype}", recursive=True)))

  for filename in list(file_set):
    with open(filename, "r") as file:
      filedata = file.read()
      filedata = re.sub(old_project_id, new_project_id, filedata)
    with open(filename, "w") as file:
      file.write(filedata)

  print(
      f"\nReplaced project_id from '{old_project_id}' to '{new_project_id}'.")
