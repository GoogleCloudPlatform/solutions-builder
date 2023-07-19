import yaml, json
from yaml.loader import SafeLoader
from jinja2 import Template
from models.task import Task, TaskStatus


class Workflow:
  workflow_path = None
  workflow = None

  def __init__(self, workflow_path):
    self.workflow_path = workflow_path
    print(f"workflow_path = {workflow_path}")

    with open(workflow_path) as f:
      self.workflow = yaml.load(f, Loader=SafeLoader)
      print(f"workflow = {self.workflow}")

  def get_next_step(self, task):
    current_complete_step = None

    # Find the current complete step in order to find the next step.
    for step in self.workflow["steps"]:
      # Found complete step, hence returning the next step object.
      if current_complete_step:
        return step

      # If not found, keep checking if the step names are the same and
      # the status is "complete".
      elif task.step == step["name"] and task.status == str(
          TaskStatus.COMPLETE.value):
        current_complete_step = step
        print(f"current_complete_step = {current_complete_step}")

    # If no current complete step found, either the next step is not ready, or
    # there's no next step.
    return None

  def get_payload(self, step, task):
    payload_str = json.dumps(step["endpoint"].get("payload"))
    payload = Template(payload_str).render(task=task.to_dict())
    return payload
