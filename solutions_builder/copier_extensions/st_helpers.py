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

import re, os, yaml
import subprocess
from jinja2.ext import Extension


# Read YAML file and convert to a dict.
def read_yaml(filepath):
  with open(filepath) as f:
    data = yaml.safe_load(f)
  return data


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


def get_project_number(project_id):
  """
    Get GCP project number based on project_id using gcloud command.
    """
  print(f"    (Retrieving project number for {project_id}...)")
  command = f"gcloud projects describe {project_id} --format='value(projectNumber)'"
  project_number = exec_gcloud_output(command)
  project_number = project_number.strip()
  if not project_number.isnumeric():
    return ""

  return project_number


def get_existing_firestore(project_id):
  """
    Get boolean whether to initialize Firestore.
    """
  print(f"   (Retrieving Firestore databases list...)")
  command = f"gcloud alpha firestore databases list --format='value(databases[0].name)' --project='{project_id}' --quiet"
  database_name = exec_gcloud_output(command)
  return database_name


def get_current_user(project_id):
  """
    Get current authenticated gcloud user.
    """
  print(f"   (Retrieving current authenticated gcloud user...)")
  command = f"gcloud config list account --format 'value(core.account)' | head -n 1"
  email = exec_gcloud_output(command)
  return email


def get_cloud_run_services(project_id):
  """
    Get all deployed Cloud Run services.
    """
  print(f"   (Retrieving existing Cloud Run services for {project_id}...)")
  command = f"gcloud run services list --format='value(name)'"
  service_names = exec_gcloud_output(command)
  service_names = re.sub(r"\n", ",", service_names)
  return service_names


def get_cluster_value(arguments):
  """
    Get a specific GKE cluster value from describe.
    """
  key, cluster_name, region = arguments
  print(f"   (Retrieving {key} from cluster {cluster_name}...)")
  command = f"gcloud container clusters describe {cluster_name} --region={region} --format='value({key})'"
  return exec_gcloud_output(command)


def get_services_from_yaml(solution_path):
  """
    Get the service list from root yaml.
    """
  st_yaml = read_yaml(f"{solution_path}/sb.yaml")
  services = []
  components = st_yaml.get("components", {})
  for component_name, properties in components.items():
    if properties.get("service_path"):
      services.append(properties["resource_name"])
  return ",".join(services)


def convert_resource_name(resource_name):
  """
    Convert to valid resource_name: lower case, alpha-numeric, dash.
    """
  resource_name = re.sub(r"\W+", "", resource_name)
  resource_name = resource_name.replace(" ", "").replace("_", "-")
  resource_name = resource_name.lower()
  if len(resource_name) > 63:
    resource_name = resource_name[:62]
  return resource_name


def assert_non_empty(value):
  assert value, "Got empty value in Copier variable."
  return value


class SolutionsTemplateHelpersExtension(Extension):

  def __init__(self, environment):
    super().__init__(environment)
    environment.filters["get_project_number"] = get_project_number
    environment.filters["get_existing_firestore"] = get_existing_firestore
    environment.filters["get_current_user"] = get_current_user
    environment.filters["get_cloud_run_services"] = get_cloud_run_services
    environment.filters["get_cluster_value"] = get_cluster_value
    environment.filters["get_services_from_yaml"] = get_services_from_yaml
    environment.filters["convert_resource_name"] = convert_resource_name
    environment.filters["assert_non_empty"] = assert_non_empty
