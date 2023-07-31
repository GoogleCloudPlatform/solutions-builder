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

template_app = typer.Typer()


@template_app.command()
def new(module_name,
        modules_folder: Annotated[
            Optional[str], typer.Argument()] = "./solutions_builder/modules",
        module_template_path=None,
        answers=None,
        yes: Optional[bool] = False):

  if not module_template_path:
    current_dir = os.path.dirname(__file__)
    module_template_path = f"{current_dir}/../module_template"

  answers_dict = get_answers_dict(answers)
  answers_dict["module_name"] = module_name
  module_path = f"{modules_folder}/{module_name}"
  run_auto(module_template_path, module_path, data=answers_dict)

  print_success(f"Complete. New module folder created at {module_path}.\n")
