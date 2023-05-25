import os
import yaml
import typer
import subprocess
import collections


def confirm(msg, skip=False, default=True):
  if not skip:
    typer.confirm(msg, abort=True, default=default)


# Check if the solution folder has st.yaml file.
def validate_solution_folder(path):
  if not os.path.isfile(path + "/st.yaml"):
    raise FileNotFoundError(
        f"Path {path} is not a valid solution folder: missing st.yaml")
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
  except:
    output = ""

  output = output.strip()
  return output


# Print success message with styling.
def print_success(msg):
  typer.echo(typer.style(msg, fg=typer.colors.GREEN, bold=True))


# Print error message with styling.
def print_error(msg):
  typer.echo(typer.style(msg, fg=typer.colors.RED, bold=True))


# Print highlighted message with styling.
def print_highlight(msg):
  typer.echo(typer.style(msg, fg=typer.colors.WHITE, bold=True))
