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

import typer, traceback, os
import importlib.metadata
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from .component import component_app
from .infra import infra_app
from .template import template_app
from .set import set_app, project_id as set_project_id
from .vars import vars_app
from .cli_utils import *
from .cli_constants import DEBUG, PLACEHOLDER_VALUES

__version__ = importlib.metadata.version("solutions-builder")
DEFAULT_DEPLOY_PROFILE = "default-deploy"

app = typer.Typer(
    add_completion=False,
    help=
    "Solutions Builder CLI. See https://github.com/GoogleCloudPlatform/solutions-builder for details."
)
app.add_typer(component_app,
              name="components",
              help="Add or update components.")
app.add_typer(component_app,
              name="component",
              help="Add or update components.")
app.add_typer(infra_app,
              name="infra",
              help="Manage infrastructure (terraform).")
app.add_typer(template_app,
              name="template",
              help="Create or update module templates.")
app.add_typer(set_app,
              name="set",
              help="Set properties to an existing solution folder.")
app.add_typer(vars_app,
              name="vars",
              help="Set variables in an existing solutions-builder folder.")


# Create a new solution
@app.command()
def new(folder_name,
        output_dir: Annotated[Optional[str], typer.Argument()] = ".",
        template_path=None,
        answers=None):
  """
  Create a new solution folder.
  """
  output_path = f"{output_dir}/{folder_name}"
  output_path = output_path.replace("//", "/")
  answers_dict = get_answers_dict(answers)

  if not template_path:
    current_dir = os.path.dirname(__file__)
    template_path = f"{current_dir}/../template_root"

  if os.path.exists(output_path):
    raise FileExistsError(f"Solution folder {output_path} already exists.")

  # Copy template_root to destination.
  print(f"template_path = {template_path}")
  answers_dict["folder_name"] = folder_name
  run_auto(template_path, output_path, data=answers_dict)

  print_success(f"Complete. New solution folder created at {output_path}.\n")


# Update a solution
@app.command()
def update(solution_path: Annotated[Optional[str],
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

  confirm(
      f"\nThis will update solution root folder at '{solution_path}'. Continue?"
  )

  # Copy template_root to destination, excluding skaffold.yaml.
  orig_sb_yaml = read_yaml(f"{solution_path}/sb.yaml")

  if not template_path:
    current_dir = os.path.dirname(__file__)
    template_path = f"{current_dir}/../template_root"
    if not os.path.exists(template_path):
      raise FileNotFoundError(f"{template_path} does not exist.")
  worker = run_auto(template_path,
                    solution_path,
                    exclude=["skaffold.yaml", "sb.yaml"])
  answers = worker.answers.last

  # Restore some fields in sb.yaml.
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  sb_yaml["created_at"] = orig_sb_yaml["created_at"]
  sb_yaml["components"] = orig_sb_yaml["components"]
  write_yaml(f"{solution_path}/sb.yaml", sb_yaml)

  print_success(f"Complete. Solution folder updated at {solution_path}.\n")


# Build and deploy services.
@app.command()
def deploy(
    profile: Annotated[str, typer.Option("--profile", "-p")] = DEFAULT_DEPLOY_PROFILE,
    component: Annotated[str, typer.Option("--component", "-c", "-m")] = None,
    namespace: Annotated[str, typer.Option("--namespace", "-n")] = None,
    dev: Optional[bool] = False,
    solution_path: Annotated[Optional[str],
                            typer.Argument()] = ".",
    skaffold_args: Optional[str] = "",
    yes: Optional[bool] = False):
  """
  Build and deploy services.
  """
  validate_solution_folder(solution_path)

  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = sb_yaml.get("global_variables", {})

  # Get project_id from sb.yaml.
  project_id = global_variables.get("project_id", None)
  assert project_id, "project_id is not set in 'global_variables' in sb.yaml."

  if project_id in PLACEHOLDER_VALUES:
    project_id = None
    while not project_id:
      project_id = input("Please set the GCP project ID: ")
    print()
    set_project_id(project_id)

    # Reload sb.yaml
    sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
    global_variables = sb_yaml.get("global_variables", {})

  # Get terraform_gke component settings.
  terraform_gke = sb_yaml["components"].get("terraform_gke")
  env_vars = {
    "PROJECT_ID": project_id,
  }
  commands = []

  if component:
    component_flag = f" -m {component} "
  else:
    component_flag = ""

  if dev:
    skaffold_command = "skaffold dev"
  else:
    skaffold_command = "skaffold run"

  if terraform_gke:
    cluster_name = terraform_gke["cluster_name"]
    region = terraform_gke["gcp_region"]
    commands.append(
        f"gcloud container clusters get-credentials {cluster_name} --region {region} --project {project_id}"
    )

  # Set Skaffold namespace
  namespace_flag = f"-n {namespace}" if namespace else ""

  # Add skaffold command.
  commands.append(
      f"{skaffold_command} -p {profile} {component_flag} {namespace_flag} --default-repo=\"gcr.io/{project_id}\" {skaffold_args}"
  )
  print("This will build and deploy all services using the command below:")
  for command in commands:
    print_success(f"- {command}")

  namespace_str = namespace or "default"
  print("\nto the namespace:")
  print_success(f"- {namespace_str}")

  print("\nwith the following environment variables:")
  env_var_str = ""
  for key, value in env_vars.items():
    print_success(f"- {key}={value}")
    env_var_str += f"{key}={value} "

  print("\nand the following global_variables from sb.yaml:")
  for key, value in sb_yaml.get("global_variables", {}).items():
    print_success(f"- {key}: {value}")

  print()
  confirm("This may take a few minutes. Continue?", skip=yes)

  for command in commands:
    exec_shell(env_var_str + command, working_dir=solution_path)

# Destory deployment.
@app.command()
def delete(profile: str = DEFAULT_DEPLOY_PROFILE,
           component: Annotated[str, typer.Option("--component", "-c", "-m")] = None,
           namespace: Annotated[str, typer.Option("--namespace", "-n")] = None,
           solution_path: Annotated[Optional[str],
                                    typer.Argument()] = ".",
           yes: Optional[bool] = False):
  """
  Delete deployment.
  """
  validate_solution_folder(solution_path)

  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = sb_yaml.get("global_variables", {})

  # Get project_id from sb.yaml.
  project_id = global_variables.get("project_id", None)
  assert project_id, "project_id is not set in 'global_variables' in sb.yaml."

  if component:
    component_flag = f" -m {component} "
  else:
    component_flag = ""

  # Set Skaffold namespace
  namespace_flag = f"-n {namespace}" if namespace else ""

  command = f"skaffold delete -p {profile} {component_flag} {namespace_flag} --default-repo=\"gcr.io/{project_id}\""
  print("This will DELETE deployed services using the command below:")
  print_highlight(command)
  confirm("\nThis may take a few minutes. Continue?", default=False, skip=yes)
  exec_shell(command, working_dir=solution_path)


@app.command()
def info(solution_path: Annotated[Optional[str],
                                    typer.Argument()] = "."):
  """
  Print info from ./sb.yaml.
  """
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  print(f"Printing info of the solution folder at '{solution_path}'\n")

  for key, value in sb_yaml.items():
    if key not in ["components", "_metadata"]:
      print(f"{key}: {value}")
  print()

  print("Installed components:")
  for key, value in sb_yaml["components"].items():
    print(f" - {key}")
  print()


@app.command()
def version():
  """
  Print version.
  """
  print(f"Solutions Builder v{__version__}")
  raise typer.Exit()


def main():
  try:
    print_highlight("Solutions Builder (version " +
                    typer.style(__version__, fg=typer.colors.CYAN, bold=True) +
                    ")\n")
    app()
    print()

  except Exception as e:
    if DEBUG:
      traceback.print_exc()
    print_error(e)
    return -1

  return 0

if __name__ == "__main__":
  main()
