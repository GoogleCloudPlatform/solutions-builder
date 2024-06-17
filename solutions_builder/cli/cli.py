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
import traceback
import os
import re
import importlib.metadata
from typing import Optional
from typing_extensions import Annotated
from copier import run_copy
from .add import add_command
from .update import update_command
from .component import list_components
from .infra import infra_app
from .template import template_app
from .set import set_app, project_id as set_project_id
from .vars import vars_app
from .cli_utils import *
from .cli_constants import DEBUG, PLACEHOLDER_VALUES

__version__ = importlib.metadata.version("solutions-builder")
DEFAULT_DEPLOY_PROFILE = "cloudrun"

app = typer.Typer(
    add_completion=False,
    help="Solutions Builder CLI. See https://github.com/GoogleCloudPlatform/solutions-builder for details."
)
app.add_typer(add_command,
              name="add",
              help="Add components.")
app.add_typer(update_command,
              name="update",
              help="Update components.")
# app.add_typer(component_app,
#               name="component",
#               help="Add or update components.")
app.add_typer(infra_app,
              name="infra",
              help="Manage infrastructure (terraform).")
app.add_typer(infra_app,
              name="terraform",
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
  run_copy(template_path, output_path, data=answers_dict, unsafe=True)

  print_success(f"Complete. New solution folder created at {output_path}.\n")


# Build and deploy services.
@app.command()
def deploy(
        profile: Annotated[str, typer.Option(
          "--profile", "-p")] = DEFAULT_DEPLOY_PROFILE,
        component: Annotated[str, typer.Option(
          "--component", "-c", "-m")] = None,
        namespace: Annotated[str, typer.Option("--namespace", "-n")] = None,
        dev: Optional[bool] = False,
        dev_cleanup: Optional[bool] = False,
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

  # Get global vars from sb.yaml.
  project_id = global_variables.get("project_id", None)
  gcp_region = global_variables.get("gcp_region", None)
  assert project_id, "project_id is not set in 'global_variables' in sb.yaml."
  assert gcp_region, "gcp_region is not set in 'global_variables' in sb.yaml."

  # Check default deploy method.
  if not profile:
    profile = global_variables.get("default_deploy_method", "cloudrun")

  # Check namespace
  deploy_config = sb_yaml.get("deploy", {})
  if deploy_config.get("require_namespace") not in [None, False, ""] \
          and not namespace:
    assert namespace, "Please set namespace with --namespace or -n"

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
  commands = []

  component_flag = f" -m {component} " if component else ""
  no_prune_flag = " --no-prune " if not dev_cleanup else ""

  port_forwarding_flag = ""
  if dev:
    skaffold_command = "skaffold dev"
    port_forwarding_flag = "--port-forward"
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

  # Set default repo to Artifact Registry
  artifact_region = "us"  # TODO: Add support to other multi-regions.
  default_repo = f"\"{artifact_region}-docker.pkg.dev/{project_id}/default\""

  # Add skaffold command.
  command_str = \
      f"{skaffold_command} -p {profile} {component_flag} {namespace_flag}" \
      f" --default-repo={default_repo}" \
      f" {skaffold_args} {port_forwarding_flag} {no_prune_flag}"
  commands.append(re.sub(" +", " ", command_str.strip()))
  print("This will build and deploy all services using the command "
        "and variables below:")
  for command in commands:
    print_success(f"- {command}")

  namespace_str = namespace or "default"
  print("\nnamespace:")
  print_success(f"- {namespace_str}")

  # print("\nenvironment variables:")
  # env_vars = {
  #   "PROJECT_ID": project_id,
  # }
  # env_var_str = ""
  # for key, value in env_vars.items():
  #   print_success(f"- {key}={value}")
  #   env_var_str += f"{key}={value} "

  print("\nglobal_variables in sb.yaml:")
  for key, value in sb_yaml.get("global_variables", {}).items():
    print_success(f"- {key}: {value}")

  print()
  confirm("This may take a few minutes. Continue?", skip=yes)
  set_gcloud_project(project_id)
  exec_shell("gcloud auth configure-docker us-docker.pkg.dev",
             working_dir=solution_path)

  for command in commands:
    exec_shell(command, working_dir=solution_path)


@ app.command()
def delete(profile: str = DEFAULT_DEPLOY_PROFILE,
           component: Annotated[str, typer.Option(
             "--component", "-c", "-m")] = None,
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

  # Get global vars from sb.yaml.
  project_id = global_variables.get("project_id", None)
  assert project_id, "project_id is not set in 'global_variables' in sb.yaml."

  component_flag = f" -m {component} " if component else ""

  # Set Skaffold namespace
  namespace_flag = f"-n {namespace}" if namespace else ""

  # Set default repo to Artifact Registry
  artifact_region = "us"  # TODO: Add support to other multi-regions.
  default_repo = f"\"{artifact_region}-docker.pkg.dev/{project_id}\""

  command = f"skaffold delete -p {profile} {component_flag} {namespace_flag}" \
            f" --default-repo={default_repo}"
  print("This will DELETE deployed services using the command below:")
  print_highlight(command)
  confirm("\nThis may take a few minutes. Continue?", default=False, skip=yes)
  exec_shell(command, working_dir=solution_path)


@ app.command()
def init(solution_path: Annotated[Optional[str], typer.Argument()] = "."):
  """
  Initialize sb.yaml for a solution folder.
  """
  components = None

  if os.path.isfile(solution_path + "/sb.yaml"):
    confirm(f"This will override the existing 'sb.yaml' in '{solution_path}'. "
            "Continue?", default=False)
    sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
    components = sb_yaml.get("components", {})

  else:
    confirm(f"This will create a new 'sb.yaml' in '{solution_path}'. "
            "Continue?", default=True)

  template_path = get_package_dir() + "/helper_modules/template_root_init"
  run_copy(template_path, solution_path, data={}, unsafe=True)

  # Restore components.
  if components:
    sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
    sb_yaml["components"] = components
    write_yaml(f"{solution_path}/sb.yaml", sb_yaml)

  print_success("Complete.")


@ app.command()
def info(solution_path: Annotated[Optional[str], typer.Argument()] = "."):
  """
  Print info from ./sb.yaml.
  """
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  print(f"Printing info of the solution folder at '{solution_path}/'\n")

  # Global variables
  print("global_variables in sb.yaml:")
  for key, value in sb_yaml.get("global_variables", {}).items():
    print(f"- {key}: {value}")
  print()

  # List of installed components.
  list_components()


@ app.command()
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
      print_error(f"Error: {e}")
    else:
      print_error(f"Error: {e}")
      print("\nTip: try adding 'DEBUG=true' to your environment variables to get more details.")
      print("E.g. DEBUG=true sb new your-project\n")

    return -1

  return 0


if __name__ == "__main__":
  main()
