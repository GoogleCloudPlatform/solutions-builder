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

import typer, time
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from .cli_utils import *

infra_app = typer.Typer()


def get_impersonate_clause(impersonate, impersonate_email, project_id):
  impersonate_clause = ""
  if impersonate:
    if not impersonate_email:
      impersonate_email = f"terraform-runner@{project_id}.iam.gserviceaccount.com"
    impersonate_clause = f"GOOGLE_IMPERSONATE_SERVICE_ACCOUNT={impersonate_email}"

  return impersonate_clause


# Project bootstrap and foundation.
@infra_app.command()
def init(solution_path: Annotated[Optional[str],
                                  typer.Argument()] = ".",
         impersonate: Optional[bool] = False,
         impersonate_email: Optional[str] = None,
         yes: Optional[bool] = False):
  validate_solution_folder(solution_path)

  if not yes:
    auto_approve_flag = ""
  else:
    auto_approve_flag = "-auto-approve"

  # Get project ID from the existing root yaml.
  st_yaml = read_yaml(f"{solution_path}/sb.yaml")
  project_id = st_yaml["project_id"]

  confirm(f"""
  This will initialize the solution with the following steps:
  - Set gcloud project to '{project_id}'
  - Run terraform init and apply in 'bootstrap' stage.
  - Run terraform init and apply in 'foundation' stage.

  This will take a few minutes. Continue?""",
          skip=yes)

  exec_shell(f"gcloud config set project {project_id}")

  working_dir = f"{solution_path}/terraform/stages/1-bootstrap"
  exec_shell(f"terraform init", working_dir=working_dir)
  exec_shell(f"terraform apply {auto_approve_flag}", working_dir=working_dir)
  exec_shell(f"terraform output > tf_output.tfvars", working_dir=working_dir)

  env_var_clause = get_impersonate_clause(impersonate, impersonate_email,
                                          project_id)
  working_dir = f"{solution_path}/terraform/stages/2-foundation"
  exec_shell(f"{env_var_clause} terraform init", working_dir=working_dir)
  exec_shell(f"{env_var_clause} terraform apply {auto_approve_flag}",
             working_dir=working_dir)
  exec_shell(f"{env_var_clause} terraform output > tf_output.tfvars",
             working_dir=working_dir)


# Project bootstrap and foundation.
@infra_app.command()
def apply(stage,
          solution_path: Annotated[Optional[str],
                                   typer.Argument()] = ".",
          impersonate_email: Optional[str] = None,
          impersonate: Optional[bool] = False,
          unlock: Optional[bool] = False,
          yes: Optional[bool] = False):
  validate_solution_folder(solution_path)
  if not yes:
    auto_approve_flag = ""
  else:
    auto_approve_flag = "-auto-approve"

  if not stage:
    print(f"Missing argument 'STAGE'. Available stages:")
    path = solution_path + "/terraform/stages"
    print("Available infra stagse:\n")
    list_subfolders(path)
    return

  stage = stage.replace("terraform/stages", "")

  confirm(f"""
  This will initialize the solution with the following steps:
  - Run terraform init and apply in '{stage}' stage.

  This will take a few minutes. Continue?""",
          skip=yes)

  # Get project_id
  st_yaml = read_yaml(f"{solution_path}/sb.yaml")
  project_id = st_yaml["project_id"]

  # Get impersonate service account email
  env_var_clause = get_impersonate_clause(impersonate, impersonate_email,
                                          project_id)
  unclock_clause = " -unlock=false" if unlock else ""
  working_dir = f"{solution_path}/terraform/stages/{stage}"
  exec_shell(f"{env_var_clause} terraform init {unclock_clause}", working_dir=working_dir)
  exec_shell(f"{env_var_clause} terraform apply {auto_approve_flag} {unclock_clause}",
             working_dir=working_dir)
  exec_shell(f"{env_var_clause} terraform output > tf_output.tfvars",
             working_dir=working_dir)


# Project bootstrap and foundation.
@infra_app.command()
def destroy(stage,
            solution_path: Annotated[Optional[str],
                                     typer.Argument()] = ".",
            impersonate_email: Optional[str] = None,
            impersonate: Optional[bool] = False,
            unlock: Optional[bool] = False,
            yes: Optional[bool] = False):
  validate_solution_folder(solution_path)
  if not yes:
    auto_approve_flag = ""
  else:
    auto_approve_flag = "-auto-approve"

  if not stage:
    print(f"Missing argument 'STAGE'. Available stages:")
    path = solution_path + "/terraform/stages"
    print("Available infra stagse:\n")
    list_subfolders(path)
    return

  stage = stage.replace("terraform/stages", "")

  confirm(f"""
  WARNING! This will destory all resources created by 'terraform/{stage}'.

  This will take a few minutes. Continue?""",
          skip=yes)

  # Get project ID from the existing root yaml.
  st_yaml = read_yaml(f"{solution_path}/sb.yaml")
  project_id = st_yaml["project_id"]

  # Get impersonate service account email
  env_var_clause = get_impersonate_clause(impersonate, impersonate_email,
                                          project_id)
  unclock_clause = " -unlock=false" if unlock else ""
  working_dir = f"{solution_path}/terraform/stages/{stage}"
  exec_shell(f"{env_var_clause} terraform init {unclock_clause}", working_dir=working_dir)
  exec_shell(f"{env_var_clause} terraform destroy {auto_approve_flag} {unclock_clause}",
             working_dir=working_dir)


@infra_app.command()
def list(solution_path: Annotated[Optional[str], typer.Argument()] = "."):
  print("Available infra stagse:\n")
  list_subfolders("./terraform/stages")
