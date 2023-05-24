import typer
import traceback
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from cli_utils import *

tool_app = typer.Typer()


@tool_app.command()
def project_number(working_dir: str = "."):
  project_id = typer.prompt("What's your GCP Project ID?")
  command = f"gcloud projects describe {project_id} --format='value(projectNumber)'"
  print("Executing the command below:")
  print(command)

  output = exec_output(command, working_dir=working_dir)
  print_highlight(output)
