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
import traceback
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from .cli_utils import *

component_app = typer.Typer()


@component_app.command()
def add(component_name,
        solution_path: Annotated[Optional[str],
                                 typer.Argument()] = "."):
  validate_solution_folder(solution_path)
  confirm(
      f"This will add component '{component_name}' to '{solution_path}'. " +
      "Continue?")
  process_component("add", component_name, solution_path)
  print_success(
      f"Complete. Component {component_name} added to solution at {solution_path}\n"
  )


@component_app.command()
def update(component_name,
           solution_path: Annotated[Optional[str],
                                    typer.Argument()] = "."):
  validate_solution_folder(solution_path)
  confirm(
      f"This will update component '{component_name}' to '{solution_path}'. " +
      "Continue?")
  process_component("update", component_name, solution_path)
  print_success(
      f"Complete. Component {component_name} updated to solution at {solution_path}\n"
  )


def update_component_to_root_yaml(component_name, solution_path):
  # Update Solution root YAML with new component name.
  solution_yaml_dict = read_yaml(f"{solution_path}/st.yaml") or {}
  components = solution_yaml_dict["components"] or {}
  components[component_name] = components.get("component_name") or {}
  solution_yaml_dict["components"] = components
  write_yaml(f"{solution_path}/st.yaml", solution_yaml_dict)


def process_component(method, component_name, solution_path):
  destination_path = "."

  # If the component name is a Git URL, use the URL as-is in copier.
  if check_git_url(component_name):
    print(f"Loading component from remote Git URL: {component_name}")
    template_path = component_name

  # Otherwise, try to locate the component in local modules/ folder.
  else:
    current_dir = os.path.dirname(__file__)
    template_path = f"{current_dir}/../modules/{component_name}"
    if not os.path.exists(template_path):
      raise FileNotFoundError(
          f"Component {component_name} does not exist in modules folder.")

    # Get destination_path defined in copier.yaml
    copier_dict = get_copier_yaml(template_path)
    destination_path = solution_path + "/" + copier_dict["_metadata"].get(
        "destination_path")
    destination_path = destination_path.replace("//", "/")

  # Get basic info from root st.yaml.
  root_st_yaml = read_yaml(f"{solution_path}/st.yaml")

  data = {
      "project_id": root_st_yaml["project_id"],
      "project_number": root_st_yaml["project_number"]
  }

  # Copy component template to destination.
  if method == "update":
    data["component_name"] = component_name
    run_auto(template_path, destination_path, data=data)
    update_component_to_root_yaml(component_name, solution_path)
  else:
    run_auto(template_path, destination_path, data=data)

  # Patch skaffold.yaml
  for patch_file in copier_dict.get("_patch", []):
    new_yaml = patch_yaml(f"{solution_path}/{patch_file}",
                          f"{solution_path}/{patch_file}.patch")
    new_yaml["requires"] = dedupe(new_yaml["requires"])
    write_yaml(f"{solution_path}/{patch_file}", new_yaml)
    os.remove(f"{solution_path}/{patch_file}.patch")


# Add specific component to the destination solution folder.
@component_app.command()
def list():
  current_dir = os.path.dirname(__file__)
  path = current_dir + "/../modules"
  print("Available modules:\n")
  list_subfolders(path)
