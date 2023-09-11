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
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from .cli_utils import *

component_app = typer.Typer()


@component_app.command()
def add(component_name,
        solution_path: Annotated[Optional[str],
                                 typer.Argument()] = ".",
        yes: Optional[bool] = False,
        answers=None):
  validate_solution_folder(solution_path)
  confirm(
      f"This will add component '{component_name}' to '{solution_path}'. " +
      "Continue?",
      skip=yes)

  answers_dict = get_answers_dict(answers)
  process_component("add", component_name, solution_path, data=answers_dict)
  print_success(
      f"Complete. Component {component_name} added to solution at {solution_path}\n"
  )


@component_app.command()
def update(component_name,
           solution_path: Annotated[Optional[str],
                                    typer.Argument()] = ".",
           yes: Optional[bool] = False,
           answers=None):
  validate_solution_folder(solution_path)
  confirm(
      f"This will update the existing component '{component_name}' in '{solution_path}'. "
      + "Continue?",
      skip=yes)

  answers_dict = get_answers_dict(answers)
  process_component("update",
                    component_name,
                    solution_path,
                    data=answers_dict,
                    use_existing_answers=yes)
  print_success(
      f"Complete. Component {component_name} updated to solution at {solution_path}\n"
  )


@component_app.command()
def init(component_name,
          solution_path: Annotated[Optional[str],
                                  typer.Argument()] = ".",
          yes: Optional[bool] = False):

  pass

@component_app.command()
def fix_skaffold(component_name,
          solution_path: Annotated[Optional[str],
                                  typer.Argument()] = ".",
          yes: Optional[bool] = False):

  pass

def update_component_to_root_yaml(component_name, answers, solution_path):
  # Update Solution root YAML with new component name.
  solution_yaml_dict = read_yaml(f"{solution_path}/sb.yaml") or {}
  components = solution_yaml_dict["components"] or {}
  components[component_name] = answers
  solution_yaml_dict["components"] = components
  write_yaml(f"{solution_path}/sb.yaml", solution_yaml_dict)


def process_component(method,
                      component_name,
                      solution_path,
                      data={},
                      use_existing_answers=False):
  destination_path = "."
  current_dir = os.path.dirname(__file__)
  answers_file = None

  # Get basic info from root sb.yaml.
  root_st_yaml = read_yaml(f"{solution_path}/sb.yaml")
  component_answers = {}

  # If the component name is a Git URL, use the URL as-is in copier.
  if check_git_url(component_name):
    print(f"Loading component from remote Git URL: {component_name}")
    template_path = component_name

  # Otherwise, try to locate the component in local modules/ folder.
  else:

    if method == "update":
      data["component_name"] = component_name
      if component_name not in root_st_yaml["components"]:
        raise NameError(
            f"Component {component_name} is not defined in the root yaml 'sb.yaml' file."
        )
      component_answers = root_st_yaml["components"][component_name]
      component_template = component_answers["component_template"]
      template_path = f"{current_dir}/../modules/{component_template}"
      answers_file = f".st/module_answers/{component_name}.yaml"

      # Use existing answer values in data, skipping the prompt.
      if use_existing_answers:
        answers_yaml = read_yaml(answers_file)
        for key, value in answers_yaml.items():
          data[key] = value

    else:
      component_template = component_name
      template_path = f"{current_dir}/../modules/{component_template}"
      if not os.path.exists(template_path):
        raise FileNotFoundError(
            f"Component {component_name} does not exist in modules folder.")

    # Get destination_path defined in copier.yaml
    copier_dict = get_copier_yaml(template_path)
    destination_path = solution_path + "/" + copier_dict["_metadata"].get(
        "destination_path")
    destination_path = destination_path.replace("//", "/")

  data["project_id"] = root_st_yaml["project_id"]
  data["project_number"] = root_st_yaml["project_number"]
  data["solution_path"] = solution_path
  data["template_path"] = template_path

  # Run copier with data.
  worker = run_auto(template_path,
                    destination_path,
                    data=data,
                    answers_file=answers_file)

  # Get answer values inputed by user.
  answers = worker.answers.user
  for key, value in worker.answers.default.items():
    if key not in answers:
      answers[key] = component_answers.get(key) or value
  answers["component_template"] = component_template
  answers["destination_path"] = copier_dict["_metadata"].get(
      "destination_path")

  # Update component's answer back to sb.yaml.
  update_component_to_root_yaml(answers["component_name"], answers,
                                solution_path)

  # Patch skaffold.yaml
  for patch_file in copier_dict.get("_patch", []):
    print(f"Patching {patch_file}...")
    new_yaml = patch_yaml(f"{solution_path}/{patch_file}",
                          f"{solution_path}/{patch_file}.patch")
    new_yaml["requires"] = dedupe(new_yaml["requires"])
    write_yaml(f"{solution_path}/{patch_file}", new_yaml)
    os.remove(f"{solution_path}/{patch_file}.patch")

  print()

# List installed components.
@component_app.command()
def list(solution_path: Annotated[Optional[str], typer.Argument()] = ".", ):
  root_st_yaml = read_yaml(f"{solution_path}/sb.yaml")
  components = root_st_yaml.get("components", [])
  print("Installed components:\n")
  for component_name, properties in components.items():
    typer.echo(
        typer.style(f"- {component_name} ", fg=typer.colors.WHITE, bold=True) +
        typer.style(f"(from: {properties['component_template']})",
                    fg=typer.colors.BLACK,
                    bold=True))
  print()


# List available components to add.
@component_app.command()
def available():
  current_dir = os.path.dirname(__file__)
  path = current_dir + "/../modules"
  print("Available components to add:\n")
  list_subfolders(path)
