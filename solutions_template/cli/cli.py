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

import typer, traceback, os
import importlib.metadata
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from pathlib import Path
from .component import component_app
from .tool import tool_app
from .infra import infra_app
from .cli_utils import *

__version__ = importlib.metadata.version("solutions-template")

app = typer.Typer(add_completion=False)
app.add_typer(component_app, name="component")
app.add_typer(tool_app, name="tool")
app.add_typer(infra_app, name="infra")


# Create a new solution
@app.command()
def new(folder_name,
        output_dir: Annotated[Optional[str], typer.Argument()] = ".",
        template_path=None,
        answers=None):
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
  if not solution_path:
    solution_path = "."

  validate_solution_folder(solution_path)

  if not os.path.exists(solution_path):
    raise FileNotFoundError(f"Solution folder {solution_path} does not exist.")

  confirm(
      f"\nThis will update solution root folder at '{solution_path}'. Continue?"
  )

  # Copy template_root to destination, excluding skaffold.yaml.
  orig_st_yaml = read_yaml(f"{solution_path}/st.yaml")

  if not template_path:
    current_dir = os.path.dirname(__file__)
    template_path = f"{current_dir}/../template_root"
    if not os.path.exists(template_path):
      raise FileNotFoundError(f"{template_path} does not exist.")
  worker = run_auto(template_path,
                    solution_path,
                    exclude=["skaffold.yaml", "st.yaml"])
  answers = worker.answers.last

  # Restore some fields in st.yaml.
  st_yaml = read_yaml(f"{solution_path}/st.yaml")
  st_yaml["created_at"] = orig_st_yaml["created_at"]
  st_yaml["components"] = orig_st_yaml["components"]
  write_yaml(f"{solution_path}/st.yaml", st_yaml)

  print_success(f"Complete. Solution folder updated at {solution_path}.\n")


# Build and deploy services.
@app.command()
def deploy(profile: str = "default",
           component: str = None,
           solution_path: Annotated[Optional[str],
                                    typer.Argument()] = ".",
           yes: Optional[bool] = False):
  validate_solution_folder(solution_path)

  solution_yaml_dict = read_yaml(f"{solution_path}/st.yaml")
  project_id = solution_yaml_dict["project_id"]

  if component:
    component_flag = f" -m {component} "
  else:
    component_flag = ""

  command = f"skaffold run -p {profile} {component_flag} --default-repo=\"gcr.io/{project_id}\""
  print("This will build and deploy all services using the command below:")
  print_highlight(command)
  confirm("\nThis may take a few minutes. Continue?", skip=yes)
  exec_shell(command, working_dir=solution_path)


# Destory services.
@app.command()
def destroy(profile: str = "default",
            component: str = None,
            solution_path: Annotated[Optional[str],
                                     typer.Argument()] = ".",
            yes: Optional[bool] = False):
  validate_solution_folder(solution_path)

  solution_yaml_dict = read_yaml(f"{solution_path}/st.yaml")
  project_id = solution_yaml_dict["project_id"]

  if component:
    component_flag = f" -m {component} "
  else:
    component_flag = ""

  command = f"skaffold delete -p {profile} {component_flag} --default-repo=\"gcr.io/{project_id}\""
  print("This will DESTROY deployed services using the command below:")
  print_highlight(command)
  confirm("\nThis may take a few minutes. Continue?", default=False, skip=yes)
  exec_shell(command, working_dir=solution_path)


@app.command()
def version():
  print(f"Solutions Template v{__version__}")
  raise typer.Exit()


def main():
  try:
    app()
    print()

  except Exception as e:
    if os.getenv("DEBUG", False):
      traceback.print_exc()
    print_error(e)


if __name__ == "__main__":
  main()