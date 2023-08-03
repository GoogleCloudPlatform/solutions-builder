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

import os, yaml, typer, subprocess, re


def confirm(msg, skip=False, default=True):
  if not skip:
    typer.confirm(msg, abort=True, default=default)


# Check if the solution folder has sb.yaml file.
def validate_solution_folder(path):
  if not os.path.isfile(path + "/sb.yaml"):
    raise FileNotFoundError(
        f"Path {path} is not a valid solution folder: missing sb.yaml")
  return True


def get_copier_yaml(path):
  filepath = f"{path}/copier.yaml"

  if not os.path.isfile(filepath):
    filepath = f"{path}/copier.yml"

  if not os.path.isfile(filepath):
    raise FileNotFoundError(
        f"Path {path} is not a valid module folder: missing copier.yaml or copier.yml"
    )

  return read_yaml(filepath)


def get_immediate_subdirectories(a_dir):
  return [
      name for name in os.listdir(a_dir)
      if os.path.isdir(os.path.join(a_dir, name))
  ]


def patch_yaml(dest_path, patch_path):
  orig_yaml = read_yaml(dest_path)
  patch_yaml = read_yaml(patch_path)
  return merge_dict(orig_yaml, patch_yaml)


# Merge two dict based on first level of properties.
def merge_dict(dict1, dict2):
  for key in dict1.keys():
    if isinstance(dict1[key], list):
      dict1[key] += dict2.get(key, [])

    elif isinstance(dict1[key], dict):
      dict1[key].update(dict2.get(key, {}))

    else:
      dict1[key] = dict2.get(key, dict1[key])

  return dict1


def dedupe(obj):
  if isinstance(obj, list):
    try:
      return [*set(obj)]
    except:
      list_map = {}
      for x in obj:
        list_map[str(x)] = x
      return [list_map[key] for key in list_map.keys()]
  else:
    return obj


# Read YAML file and convert to a dict.
def read_yaml(filepath):
  with open(filepath) as f:
    data = yaml.safe_load(f)
  return data


# Write a dict as a YAML file.
def write_yaml(filepath, dict_data):
  with open(filepath, "w") as f:
    yaml.dump(dict_data, f)


# Execute shell commands
def exec_shell(command, working_dir=".", stop_when_error=True, stdout=None):
  proc = subprocess.Popen(command, cwd=working_dir, shell=True, stdout=stdout)
  exit_status = proc.wait()

  if exit_status != 0 and stop_when_error:
    raise Exception(
        f"Error when running command: {command} (working_dir={working_dir})")

  return exit_status


# Execute shell commands
def exec_output(command, working_dir=".", stop_when_error=True):
  output = subprocess.check_output(command,
                                   cwd=working_dir,
                                   shell=True,
                                   text=True)
  return output


def exec_gcloud_output(command, working_dir="."):
  output = ""
  try:
    output = exec_output(command)
  except Exception as e:
    print(f"Error: {e}")
    output = ""

  output = output.strip()
  return output


def list_subfolders(path):
  modules = get_immediate_subdirectories(path)
  for module_name in sorted(modules):
    print_highlight(f"- {module_name}")
  print()


def check_git_url(url):
  regex_str = "((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?"
  regex = re.compile(regex_str)
  match = regex.match(url)
  return match is not None


def get_answers_dict(data):
  if data:
    return dict(s.split("=") for s in data.split(","))
  else:
    return {}


def get_project_number(project_id):
  """
    Get GCP project number based on project_id using gcloud command.
    """
  print(f"(Retrieving project number for {project_id}...)")
  command = f"gcloud projects describe {project_id} --format='value(projectNumber)'"
  project_number = exec_gcloud_output(command)
  project_number = project_number.strip()
  if not project_number.isnumeric():
    return ""

  return project_number


# Print success message with styling.
def print_success(msg):
  typer.echo(typer.style(msg, fg=typer.colors.GREEN, bold=True))


# Print error message with styling.
def print_error(msg):
  typer.echo(typer.style(msg, fg=typer.colors.RED, bold=True))


# Print highlighted message with styling.
def print_highlight(msg):
  typer.echo(typer.style(msg, fg=typer.colors.WHITE, bold=True))
