import pytest, requests, time
from models.task import Task, TaskStatus
from workflow.workflow import Workflow
import os

current_dir = os.path.dirname(__file__)
WORKFLOW_PATH = f"{current_dir}/example.yaml"


@pytest.fixture
def fake_task():
  task_data = {
      "title": "Title",
      "description": "Description",
      "step": "step-1",
      "status": "complete",
      "created_at": "2023-07-07 18:58:50.149278",
      "modified_at": "2023-07-07 18:58:50.149300",
      "data": "test data",
      "id": "fake_id"
  }
  return Task.from_dict(task_data)


def test_get_next_step(fake_task):
  workflow = Workflow(WORKFLOW_PATH)
  next_step = workflow.get_next_step(fake_task)
  print(next_step)

  assert next_step["name"] == "step-2"
