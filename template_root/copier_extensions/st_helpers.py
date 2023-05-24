import re
import unicodedata

from jinja2.ext import Extension
from cli_utils import exec_output


# taken from Django
# https://github.com/django/django/blob/main/django/utils/text.py
def get_project_number(project_id):
  """
    Get GCP project number based on project_id using gcloud command.
    """
  print(f"    (Retrieving project number for {project_id}...)")
  project_number = ""
  try:
    project_id = str(project_id)
    if project_id:
      command = f"gcloud projects describe {project_id} --format='value(projectNumber)'"
      project_number = exec_output(command)
  except:
    project_number = ""

  project_number = project_number.strip()
  if not project_number.isnumeric():
    return ""

  return project_number


class SolutionsTemplateHelpersExtension(Extension):

  def __init__(self, environment):
    super().__init__(environment)
    environment.filters["get_project_number"] = get_project_number
