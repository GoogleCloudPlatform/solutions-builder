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
import git
import shutil
from typing import Optional
from typing_extensions import Annotated
from copier import run_copy
from .cli_utils import *


def add_component(component_name,
                  template_path: Annotated[str,
                                           typer.Option("--template", "-t")] = None,
                  solution_path: Annotated[Optional[str],
                                           typer.Argument()] = ".",
                  destination_path: Annotated[str,
                                              typer.Option("--dest", "-d")] = "components",
                  yes: Optional[bool] = False,
                  answers=None):
  # validate_solution_folder(solution_path)

  # Check if template_path is empty.
  if not template_path:
    print("Please set --template or -t to a local folder path, "
          "remote git repo, or one of modules below:")
    list_component_templates()
    return

  confirm(
      f"This will add component '{component_name}' to "
      f"'{destination_path}' folder. Continue?",
      skip=yes)

  answers_dict = get_answers_dict(answers)
  answers_dict["destination_path"] = destination_path
  process_component("add",
                    component_name, template_path,
                    solution_path, destination_path, data=answers_dict)
  print_success(
      f"Complete. Component {component_name} added to solution at {solution_path}\n"
  )


def update_component(component_name,
                     solution_path: Annotated[Optional[str],
                                              typer.Argument()] = ".",
                     destination_path: Annotated[str,
                                                 typer.Option("--dest", "-d")] = "components",
                     yes: Optional[bool] = False,
                     answers=None):
  validate_solution_folder(solution_path)
  confirm(
      f"This will update '{component_name}' in "
      f"'{solution_path}/components'. Continue?",
      skip=yes)

  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  components = sb_yaml.get("components", {})
  component_dict = components.get(component_name, {})
  template_path = component_dict.get("template_path")

  answers_dict = get_answers_dict(answers)
  process_component("update",
                    component_name,
                    template_path,
                    solution_path,
                    destination_path,
                    data=answers_dict,
                    use_existing_answers=yes)
  print_success(
      f"Complete. Component {component_name} updated.\n"
  )


def update_root_yaml(component_name, answers, solution_path):
  # Update Solution root YAML with new component name.
  solution_yaml_dict = read_yaml(f"{solution_path}/sb.yaml") or {}
  components = solution_yaml_dict.get("components", {})
  components[component_name] = answers
  solution_yaml_dict["components"] = components

  # Update global variables.
  global_variables = solution_yaml_dict.get("global_variables", {})
  if "project_id" in answers:
    global_variables["project_id"] = answers["project_id"]
  if "project_number" in answers:
    global_variables["project_number"] = answers["project_number"]
  solution_yaml_dict["global_variables"] = global_variables

  write_yaml(f"{solution_path}/sb.yaml", solution_yaml_dict)


def process_component(method,
                      component_name,
                      template_path,
                      solution_path,
                      destination_path,
                      data={},
                      use_existing_answers=False):

  assert template_path, "template_path is empty."
  current_dir = os.path.dirname(__file__)
  template_dir = f"{current_dir}/../modules/{template_path}"
  answers_file = None

  # Get basic info from root sb.yaml.
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = sb_yaml.get("global_variables", {})
  component_answers = {}

  # If the component name is a Git URL, use the URL as-is in copier.
  if check_git_url(template_path):
    template_dir = clone_remote_git(template_path)

  # Otherwise, try to locate the component in local modules/ folder.
  else:
    if method == "update":
      data["component_name"] = component_name
      if component_name not in sb_yaml["components"]:
        raise NameError(
            f"Component {component_name} is not defined in the root yaml 'sb.yaml' file."
        )
      component_answers = sb_yaml["components"][component_name]
      template_path = component_answers["template_path"]
      answers_file = f".sb/module_answers/{component_name}.yaml"

      # Use existing answer values in data, skipping the prompt.
      if use_existing_answers:
        answers_yaml = read_yaml(answers_file)
        for key, value in answers_yaml.items():
          data[key] = value

    else:
      template_dir = f"{current_dir}/../modules/{template_path}"
      if not os.path.exists(template_dir):
        # If module does not exist in the solutions-builder package,
        # try loading from the local file path.
        template_dir = template_path
        if not os.path.exists(template_dir):
          raise FileNotFoundError(
              f"Component '{template_path}' does not exist.")

    # # Get destination_path defined in copier.yaml
    # destination_path = solution_path + "/" + copier_dict["_metadata"].get(
    #     "destination_path")
    # destination_path = destination_path.replace("//", "/")

  copier_dict = get_copier_yaml(template_dir)
  data["component_name"] = component_name
  if "project_id" in data:
    data["project_id"] = global_variables.get("project_id")
  if "project_number" in data:
    data["project_number"] = global_variables.get("project_number")
  data["solution_path"] = solution_path
  data["template_path"] = template_path

  # Run copier with data.
  worker = run_copy(template_dir,
                    ".",
                    data=data,
                    answers_file=answers_file,
                    unsafe=True)

  # Get answer values inputed by user.
  answers = worker.answers.user

  for key, value in worker.answers.user_defaults.items():
    if key not in answers:
      answers[key] = component_answers.get(key) or value
  answers["template_path"] = template_path
  answers["destination_path"] = destination_path

  # Update component's answer back to sb.yaml.
  update_root_yaml(component_name,
                   answers,
                   solution_path)

  # Patch skaffold.yaml
  for patch_file in copier_dict.get("_patch", []):
    print(f"Patching {patch_file}...")
    new_yaml = patch_yaml(f"{solution_path}/{patch_file}",
                          f"{solution_path}/{patch_file}.patch")
    new_yaml["requires"] = dedupe(new_yaml.get("requires"))
    write_yaml(f"{solution_path}/{patch_file}", new_yaml)
    os.remove(f"{solution_path}/{patch_file}.patch")

  print()


def list_components(solution_path: Annotated[Optional[str], typer.Argument()] = "."):
  """List installed components."""
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  components = sb_yaml.get("components", [])
  print("Installed components:")
  for component_name, properties in components.items():
    typer.echo(
        typer.style(f"- {component_name} ", fg=typer.colors.WHITE, bold=True) +
        typer.style(f"(template: {properties['template_path']})",
                    fg=typer.colors.BLACK,
                    bold=True))
  print()


# List available components to add.
def list_available_components():
  print("Available components to add:\n")
  list_component_templates()
