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
from .cli_utils import *

infra_app = typer.Typer()


# Apply terraform stage(s)
@infra_app.command()
def apply(stage: Annotated[Optional[str],
                           typer.Argument()] = None,
          solution_path: Optional[str] = ".",
          impersonate_email: Optional[str] = None,
          unlock: Optional[bool] = False,  # Whether to unlock existing stages.
          all_stages: Annotated[bool, typer.Option("--all")] = None,
          yes: Optional[bool] = False,
          debug: Optional[bool] = False):
  validate_solution_folder(solution_path)

  if all_stages:
    # Get all stage folders in './terraform/stages'
    terraform_stages = get_immediate_subdirectories(
        f"{solution_path}/terraform/stages")

  elif stage:
    terraform_stages = [stage.replace("terraform/stages", "")]

  else:
    print(f"Missing argument 'STAGE' or '--all'. Available stages:")
    path = solution_path + "/terraform/stages"
    print("Available terraform (infra) stages:\n")
    list_subfolders(path)
    return

  terraform_stage_str = "\n".join(
    [f"    - {stage}" for stage in terraform_stages])

  confirm(f"""
  This will initialize the solution with the following steps:
  - Run terraform init and apply in the following stage(s):
{terraform_stage_str}

  This may take a few minutes. Continue?""",
          skip=yes)

  # Get project ID from the existing root yaml.
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = sb_yaml.get("global_variables", {})
  project_id = global_variables.get("project_id")
  set_gcloud_project(project_id)

  # Init and apply in a specific stage folder.
  for stage in terraform_stages:
    print("\n")
    terraform_apply(solution_path, stage, unlock, yes,
                    impersonate_email, project_id)


@infra_app.command("import")
def import_resource(stage, resource_path, destination_path,
                    yes: Optional[bool] = False,
                    solution_path: Annotated[Optional[str],
                                             typer.Argument()] = "."):
  """Import terraform resource(s)"""

  confirm(f"""
  This will import the resource '{resource_path}' to '{stage}' stage.
  Continue?""",
          skip=yes)

  # Get project ID from the existing root yaml.
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = sb_yaml.get("global_variables", {})
  project_id = global_variables.get("project_id")
  set_gcloud_project(project_id)

  working_dir = f"{solution_path}/terraform/stages/{stage}"
  exec_shell(
    f"terraform import {resource_path} {project_id}/{destination_path}",
      working_dir=working_dir)


@infra_app.command()
def destroy(stage: Annotated[Optional[str],
                             typer.Argument()] = None,
            solution_path: Optional[str] = ".",
            impersonate_email: Optional[str] = None,
            unlock: Optional[bool] = False,
            yes: Optional[bool] = False):
  """Destroy a terraform stage"""
  validate_solution_folder(solution_path)

  if not stage:
    print(f"Missing argument 'STAGE'. Available stages:")
    path = solution_path + "/terraform/stages"
    print("Available terraform (infra) stages:\n")
    list_subfolders(path)
    return

  if not yes:
    auto_approve_flag = ""
  else:
    auto_approve_flag = "-auto-approve"

  if not stage:
    print(f"Missing argument 'STAGE'. Available stages:")
    path = solution_path + "/terraform/stages"
    print("Available terraform (infra) stages:\n")
    list_subfolders(path)
    return

  stage = stage.replace("terraform/stages", "")

  confirm(f"""
  WARNING!!
  This will destory all resources created in 'terraform/stages/{stage}'.

  Continue?""", skip=yes)

  # Get project ID from the existing root yaml.
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = sb_yaml.get("global_variables", {})
  project_id = global_variables.get("project_id")
  set_gcloud_project(project_id)

  # Get impersonate service account email
  env_var_clause = get_impersonate_clause(
    project_id, impersonate_email) if impersonate_email else ""

  # Get unlock flag
  unclock_clause = " -unlock=false" if unlock else ""

  # Destroy a terraform stage
  working_dir = f"{solution_path}/terraform/stages/{stage}"
  exec_shell(f"{env_var_clause} terraform init {unclock_clause}",
             working_dir=working_dir)
  exec_shell(f"{env_var_clause} terraform destroy {auto_approve_flag} "
             f"{unclock_clause}", working_dir=working_dir)


@infra_app.command()
def list(solution_path: Annotated[Optional[str], typer.Argument()] = "."):
  print("Available terraform (infra) stages:\n")
  list_subfolders(f"{solution_path}/terraform/stages")


def get_impersonate_clause(project_id, impersonate_email: str = None):
  impersonate_clause = ""
  if not impersonate_email:
    impersonate_email = f"terraform-runner@{project_id}.iam.gserviceaccount.com"
  impersonate_clause = f"GOOGLE_IMPERSONATE_SERVICE_ACCOUNT={impersonate_email}"
  return impersonate_clause


def terraform_apply(solution_path, stage, unlock=False,
                    yes=False, impersonate_email=None, project_id=None):

  # Get auto-approve flag.
  auto_approve_flag = "-auto-approve" if yes else ""

  # Get impersonate service account email
  env_var_clause = get_impersonate_clause(
    project_id, impersonate_email) if impersonate_email else ""

  # Get unlock flag
  unclock_clause = " -lock=false" if unlock else ""

  # Init and apply in a specific stage folder.
  print(f"Applying Terraform stage: '{stage}'...")
  working_dir = f"{solution_path}/terraform/stages/{stage}"
  exec_shell(f"{env_var_clause} terraform init {unclock_clause}",
             working_dir=working_dir)
  exec_shell(f"{env_var_clause} terraform apply {auto_approve_flag} {unclock_clause}",
             working_dir=working_dir)
  exec_shell(f"{env_var_clause} terraform output > tf_output.tfvars",
             working_dir=working_dir)
