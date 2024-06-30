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

import os
import yaml
import typer
import subprocess
import re
import shutil
import git
from copier import run_copy
from .cli_constants import DEBUG


def confirm(msg, skip=False, abort=True, default=True):
  if skip:
    return True

  return typer.confirm(msg, abort=abort, default=default)


def validate_solution_folder(path):
  """Check if the solution folder has sb.yaml file."""
  if not os.path.isfile(path + "/sb.yaml"):
    confirm(
        f"Path {path} is not a valid solution folder: missing sb.yaml.\n"
        "Do you want to initialize with a new `sb.yaml`?")
    run_module_template("init_sb_yaml", modules_dir="helper_modules")

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
  return sorted([
      name for name in os.listdir(a_dir)
      if os.path.isdir(os.path.join(a_dir, name))
  ])


def patch_yaml(dest_path, patch_path):
  orig_yaml = read_yaml(dest_path)
  patch_yaml = read_yaml(patch_path)
  return merge_dict(orig_yaml, patch_yaml)


def merge_dict(dict1, dict2):
  """Merge two dict based on first level of properties."""
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


def read_yaml(filepath):
  """Read YAML file and convert to a dict."""
  try:
    with open(filepath) as f:
      data = yaml.safe_load(f)
    return data
  except FileNotFoundError as e:
    return {}


def write_yaml(filepath, dict_data):
  """Write a dict as a YAML file"""
  with open(filepath, "w") as f:
    yaml.dump(dict_data, f)


def exec_shell(command, working_dir=".", stop_when_error=True, stdout=None):
  """Execute shell commands"""
  proc = subprocess.Popen(command, cwd=working_dir, shell=True, stdout=stdout)
  exit_status = proc.wait()

  if exit_status != 0 and stop_when_error:
    raise RuntimeError(
        f"Error occurs when running command: {command} (working_dir={working_dir})")

  return exit_status


def exec_output(command, working_dir=".", stop_when_error=True):
  """Execute shell commands"""
  output = subprocess.check_output(command,
                                   cwd=working_dir,
                                   shell=True,
                                   text=True)
  print(output)
  return output


def exec_gcloud_output(command, working_dir=".", hide_error=False):
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
  for module_name in modules:
    print_highlight(f"- {module_name}")
  print()


def list_component_templates():
  current_dir = os.path.dirname(__file__)
  path = current_dir + "/../modules"
  list_subfolders(path)


def check_git_url(url):
  regex_str = "((git|ssh|http(s)?)|(git@[\\w\\.]+))(:(//)?)([\\w\\.\\@\\:/\\-~]+)(\\.git)(/)?"
  regex = re.compile(regex_str)
  match = regex.match(url)
  return match is not None


def clone_remote_git(source_url):
  git_url, git_subfolder = source_url.split(".git")
  git_url += ".git"
  current_dir = os.path.dirname(__file__)
  dest_dir = current_dir + "/../downloaded_repos/" + git_url

  if os.path.exists(dest_dir):
    if confirm(
      f"🎤 Git repo '{git_url}' has been downloaded before. \n   "
            "Do you want to re-download it?", abort=False):
      shutil.rmtree(dest_dir)
      git.Repo.clone_from(git_url, dest_dir)
  else:
    git.Repo.clone_from(git_url, dest_dir)

  print()
  return dest_dir + "/" + git_subfolder


def get_package_dir():
  current_dir = os.path.dirname(__file__)
  return current_dir + "/../"


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
  project_number = exec_gcloud_output(command, hide_error=True)
  project_number = project_number.strip()
  if not project_number.isnumeric():
    return ""

  return project_number


def set_gcloud_project(project_id):
  """
    Set GCP project based on project_id using gcloud command.
    """
  if project_id:
    print(f"(Setting gcloud to project '{project_id}'...)")
    exec_gcloud_output(f"gcloud config set project {project_id} --quiet")


def create_default_artifact_repo(project_id, repo_name, region="us"):
  """
    Create default artifact repository.
  """
  print(f"(Creating default artifact repository...)")
  exec_gcloud_output(f"gcloud config set project {project_id}")
  exec_gcloud_output(
    f"gcloud artifacts repositories create {repo_name}"
    f" --repository-format=docker --location={region}")


def set_debug_flag(is_debug):
  DEBUG = is_debug


def verify_copier_file(path):
  "Check if copier.yaml exists in folder path"
  if not os.path.isfile(path + "/copier.yaml"):
    confirm(f"No copier.yaml found in {path}. Do you still want to continue?")


def update_global_var(var_name, var_value, solution_path="."):
  """
    Update global variable.
    """
  sb_yaml = read_yaml(f"{solution_path}/sb.yaml")
  global_variables = sb_yaml.get("global_variables", {})
  global_variables[var_name] = var_value
  sb_yaml["global_variables"] = global_variables
  write_yaml(f"{solution_path}/sb.yaml", sb_yaml)


def run_module_template(module_name, modules_dir="modules",
                        dest_dir=".", data={}, answers_file=None):
  """
    Run module template.
    """
  print(f"Adding module '{module_name}'...\n")

  current_dir = os.path.dirname(__file__)
  template_dir = f"{current_dir}/../{modules_dir}/{module_name}"
  worker = run_copy(template_dir,
                    dest_dir,
                    data=data,
                    answers_file=answers_file,
                    unsafe=True)
  return worker.answers.user


def print_success(msg):
  """Print success message with styling."""
  typer.echo(typer.style(msg, fg=typer.colors.GREEN, bold=True))


# Print error message with styling.
def print_error(msg):
  typer.echo(typer.style(msg, fg=typer.colors.RED, bold=True))


# Print highlighted message with styling.
def print_highlight(msg):
  typer.echo(typer.style(msg, fg=typer.colors.WHITE, bold=True))
