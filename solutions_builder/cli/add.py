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
from copier import run_copy
from .cli_utils import *
from .component import add_component

add_command = typer.Typer()


@add_command.command()
def component(component_name,
              template_path: Annotated[str,
                                       typer.Option("--template", "-t")] = None,
              solution_path: Annotated[Optional[str],
                                       typer.Argument()] = ".",
              destination_path: Annotated[str,
                                          typer.Option("--dest", "-d")] = "components",
              yes: Optional[bool] = False,
              answers=None):
  add_component(component_name, template_path,
                solution_path, destination_path, yes, answers)


@add_command.command()
def infra(module_name,
          solution_path: Annotated[Optional[str],
                                   typer.Argument()] = ".",
          yes: Optional[bool] = False,
          answers=None):
  add_component(module_name, module_name,
                solution_path, ".", yes, answers)
