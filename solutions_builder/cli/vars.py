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
import pathlib
import re
import jinja2
from typing import Optional
from typing_extensions import Annotated
from copier import run_auto
from .cli_utils import *

vars_app = typer.Typer()

INCLUDE_PATTERNS = [
    "*.yaml", "*.yml", "*.env", "*.tfvars", "*.tf", "*.sh", "*.md"
]
EXCLUDE_PATTERNS = ["**/.terraform/**/*.*", "**/node_modules/**/*.*", "**/.venv/**/*.*"]

# Replace a varialbe with a given text content.
def replace_var_to_template(var_name, text, custom_template=False, debug=False):
  match_pattern = f"^([^\\r]*[:|=]\\s*)([\"\']?)([^\"^\']*)([\"\']?)\\s*#\\s*sb-var:{var_name}"
  output_pattern = f"\\1\\2{{{{{var_name}}}}}\\4 # sb-var:{var_name}"

  if custom_template:
    match_pattern = match_pattern + ":(.*)"
    output_pattern = f"\\1\\2\\5\\4 # sb-var:{var_name}:\\5"

  if debug:
    print(f"match_pattern = {match_pattern}")

  text, count = re.subn(match_pattern, output_pattern, text)
  return (text, count)

def restore_template_in_comment(var_name, var_value, text):
  # Restore jinja2 variables in the custom content comment.
  match_pattern = f"(#\\s*sb-var:{var_name}:)(.*){var_value}(.*)"
  output_pattern = f"\\1\\2{{{{{var_name}}}}}\\3"
  text, count = re.subn(match_pattern, output_pattern, text)
  return (text, count)


def replace_var_to_value(var_name, var_value, text):
  overall_count = 0

  # Replace simple variable pattern with sb-var:var_name
  text, count = replace_var_to_template(var_name, text)
  overall_count += count

  # Replace custom-content variable pattern with sb-var:var_name:custom_template
  text, count = replace_var_to_template(var_name, text, custom_template=True)
  overall_count += count

  # Update variables using Jinja2
  jinja_env = jinja2.Environment()
  text = text.replace("# copier:raw", "# copier:raw{% raw %}")
  text = text.replace("# copier:endraw", "# copier:endraw{% endraw %}")
  template = jinja_env.from_string(text)

  # Set vars data for jinja
  data = {}
  data[var_name] = var_value

  # Apply variable values using Jinja2
  text = template.render(**data)

  # Restore vars to template in comment.
  text, count = restore_template_in_comment(var_name, var_value, text)

  return (text, overall_count)

# Apply a specific variable with a new value.
def apply_var_to_folder(solution_path, var_name, var_value):
  file_set = set()

  # Adding includes.
  for pattern in INCLUDE_PATTERNS:
    file_list = pathlib.Path(solution_path).rglob(f"{pattern}")
    file_set.update(set([str(x) for x in file_list]))

  # Removing excludes.
  for pattern in EXCLUDE_PATTERNS:
    file_list = pathlib.Path(solution_path).rglob(f"{pattern}")
    file_set = file_set - set([str(x) for x in file_list])

  modified_files_list = []
  for filename in list(file_set):
    with open(filename, "r") as file:
      # Replace variable
      filedata = file.read()
      filedata, count = replace_var_to_value(var_name, var_value, filedata)
      filedata = filedata + "\n"

      if count > 0:
        modified_files_list.append(filename)

      # If there's any changes, write back to the original file.
      if count > 0:
        with open(filename, "w") as file:
          file.write(filedata)

  return modified_files_list

# CLI command for `sb vars set <var_name> <var_value>`
@vars_app.command(name="set")
def set_var(
    var_name,
    var_value,
    solution_path: Annotated[Optional[str], typer.Argument()] = ".",
):
  validate_solution_folder(solution_path)

  # Update to the root sb.yaml
  root_st_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = root_st_yaml.get("global_variables", {})
  global_variables[var_name] = var_value
  root_st_yaml["global_variables"] = global_variables
  write_yaml(f"{solution_path}/sb.yaml", root_st_yaml)

  # Apply vars to individual files
  filenames = apply_var_to_folder(solution_path, var_name, var_value)

  print_success(
      f"Complete. {len(filenames)} files updated.\n"
  )
