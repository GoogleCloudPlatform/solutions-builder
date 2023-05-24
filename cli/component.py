import typer
import traceback
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from cli_utils import *

component_app = typer.Typer()


@component_app.command()
def add(component_name,
        solution_path: Annotated[Optional[str],
                                 typer.Argument()] = "."):
  validate_solution_folder(solution_path)

  confirm(f"This will add component '{component_name}' to {solution_path}. " +
          "Continue?")

  # TODO: Update this to comply with git path.
  cwd = os.getcwd()
  template_folder = f"{cwd}/modules/{component_name}"
  if not os.path.exists(template_folder):
    raise FileNotFoundError(
        f"Component {component_name} does not exist in modules folder.")

  # Get destination_path defined in copier.yaml
  copier_dict = get_copier_yaml(template_folder)
  destination_path = solution_path + "/" + copier_dict["_metadata"].get(
      "destination_path")
  destination_path = destination_path.replace("//", "/")

  # Update Solution root YAML with new component name.
  solution_yaml_dict = read_yaml(f"{solution_path}/st.yaml")
  if not solution_yaml_dict:
    solution_yaml_dict = {}

  component_list = solution_yaml_dict.get("components", [])
  component_list.append(component_name)
  component_list = dedupe(component_list)
  solution_yaml_dict["components"] = component_list
  write_yaml(f"{solution_path}/st.yaml", solution_yaml_dict)

  # Copy component template to destination.
  run_auto(template_folder,
           destination_path,
           data={
               "component_name": component_name,
           })

  # Patch skaffold.yaml
  for patch_file in copier_dict.get("_patch", []):
    new_yaml = patch_yaml(f"{solution_path}/{patch_file}",
                          f"{solution_path}/{patch_file}.patch")
    new_yaml["requires"] = dedupe(new_yaml["requires"])
    write_yaml(f"{solution_path}/{patch_file}", new_yaml)
    os.remove(f"{solution_path}/{patch_file}.patch")

  print_success(
      f"Complete. Component {component_name} added to solution at {solution_path}\n"
  )


# Add specific component to the destination solution folder.
@component_app.command()
def list():
  path = os.getcwd() + "/modules"
  modules = get_immediate_subdirectories(path)

  print("Available module names:\n")
  for module_name in modules:
    print_highlight(f"- {module_name}")
  print()
