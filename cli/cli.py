import typer
import traceback
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from component import component_app
from tool import tool_app
from cli_utils import *

state = {"debug": False}

app = typer.Typer()
app.add_typer(component_app, name="component")
app.add_typer(tool_app, name="tool")


# Create a new solution
@app.command()
def new(folder_name, output_dir):
  output_path = f"{output_dir}/{folder_name}"
  output_path = output_path.replace("//", "/")
  cwd = os.getcwd()
  template_folder = f"{cwd}/template_root"

  if os.path.exists(output_path):
    raise FileExistsError(f"Solution folder {output_path} already exists.")

  # Copy template_root to destination.
  run_auto(template_folder, output_path, data={
      "folder_name": folder_name,
  })

  print_success(f"Complete. New solution folder created at {output_path}.\n")


# Update a solution
@app.command()
def update(solution_path):
  validate_solution_folder(solution_path)

  cwd = os.getcwd()
  template_folder = f"{cwd}/template_root"

  if not os.path.exists(solution_path):
    raise FileNotFoundError(f"Solution folder {solution_path} does not exist.")

  confirm(
      f"\nThis will update solution folder at '{solution_path}'. Continue?")

  # Copy template_root to destination, excluding skaffold.yaml.
  orig_st_yaml = read_yaml(f"{solution_path}/st.yaml")
  run_auto(template_folder, solution_path, exclude=["skaffold.yaml"])

  # Restore some fields in st.yaml.
  st_yaml = read_yaml(f"{solution_path}/st.yaml")
  st_yaml["created_at"] = orig_st_yaml["created_at"]
  st_yaml["components"] = orig_st_yaml["components"]
  write_yaml(f"{solution_path}/st.yaml", st_yaml)

  print_success(f"Complete. Solution folder updated at {solution_path}.\n")


# Project bootstrap and foundation.
@app.command()
def init(solution_path: Annotated[Optional[str],
                                  typer.Argument()] = ".",
         yes: Optional[bool] = False,
         stage=None):
  validate_solution_folder(solution_path)
  if not yes:
    auto_approve_flag = ""
  else:
    auto_approve_flag = "-auto-approve"

  if not stage:
    confirm(f"""
  This will initialize the solution with the following steps:
  - Run terraform init and apply in 'bootstrap' stage.
  - Run terraform init and apply in 'foundation' stage.

  This will take a few minutes. Continue?""",
            skip=yes)

    working_dir = f"{solution_path}/terraform/stages/1-bootstrap"
    exec_shell(f"terraform init", working_dir=working_dir)
    exec_shell(f"terraform apply {auto_approve_flag}", working_dir=working_dir)
    exec_shell(f"terraform output > tf_output.tfvars", working_dir=working_dir)

    working_dir = f"{solution_path}/terraform/stages/2-foundation"
    exec_shell(f"terraform init", working_dir=working_dir)
    exec_shell(f"terraform apply {auto_approve_flag}", working_dir=working_dir)
    exec_shell(f"terraform output > tf_output.tfvars", working_dir=working_dir)

  else:
    confirm(f"""
  This will initialize the solution with the following steps:
  - Run terraform init and apply in '{stage}' stage.

  This will take a few minutes. Continue?""",
            skip=yes)

    working_dir = f"{solution_path}/terraform/stages/{stage}"
    exec_shell(f"terraform init", working_dir=working_dir)
    exec_shell(f"terraform apply {auto_approve_flag}", working_dir=working_dir)
    exec_shell(f"terraform output > tf_output.tfvars", working_dir=working_dir)


# Build and deploy services.
@app.command()
def deploy(profile: str = "default",
           solution_path: Annotated[Optional[str],
                                    typer.Argument()] = ".",
           yes: Optional[bool] = False):
  validate_solution_folder(solution_path)

  solution_yaml_dict = read_yaml(f"{solution_path}/st.yaml")
  project_id = solution_yaml_dict["project_id"]

  command = f"skaffold run -p {profile} --default-repo=\"gcr.io/{project_id}\""
  print("This will build and deploy all services using the command below:")
  print_highlight(command)
  confirm("\nThis may take a few minutes. Continue?", skip=yes)
  exec_shell(command, working_dir=solution_path)


@app.callback()
def callback(debug: bool = False):
  """
    Manage users in the awesome CLI app.
    """
  if debug:
    state["debug"] = True


if __name__ == "__main__":
  try:
    app()
    print()

  except Exception as e:
    if state["debug"]:
      traceback.print_exc()
    print_error(e)
