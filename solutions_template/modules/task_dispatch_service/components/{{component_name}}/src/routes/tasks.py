"""
Copyright 2022 Google LLC

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

import requests
import datetime
from fastapi import APIRouter, HTTPException
from models.task import Task
from schemas.task import TaskSchema
from utils.workflow_helper import *

# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/task", tags=["task"])

SUCCESS_RESPONSE = {"status": "Success"}


@router.get("/{id}", response_model=TaskSchema)
async def get(id: str):
  """Get a Task

  Args:
    id (str): unique id of the task

  Raises:
    HTTPException: 404 Not Found if task doesn't exist for the given task id
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [task]: task object for the provided task id
  """
  task = Task.find_by_id(id)

  if task is None:
    raise HTTPException(status_code=404, detail=f"Task {id} not found.")
  return task


@router.post("")
async def post(data: TaskSchema):
  """Create a Task

  Args:
    data (Task): Required body of the task

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: task ID of the task if the task is successfully created
  """
  id = data.id
  existing_task = Task.find_by_id(id)

  if existing_task:
    raise HTTPException(status_code=409, detail=f"Task {id} already exists.")

  new_task = Task()
  new_task = new_task.from_dict({**data.dict()})
  new_task.created_at = datetime.datetime.utcnow()
  new_task.modified_at = datetime.datetime.utcnow()
  new_task.save()

  return SUCCESS_RESPONSE


@router.put("")
async def put(data: TaskSchema):
  """Update a Task

  Args:
    data (Task): Required body of the task

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the task is updated
  """
  id = data.id
  task = Task.find_by_id(id)

  if task:
    task = task.from_dict({**data.dict()})
    task.modified_at = datetime.datetime.utcnow()
    task.save()

  else:
    raise HTTPException(status_code=404, detail=f"Task {id} not found.")

  return SUCCESS_RESPONSE


@router.post("/{id}")
async def complete(id: str):
  """Mark a Task as completed.

  Args:
    id (str): unique id of the task

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the task is deleted
  """

  task = Task.find_by_id(id)

  if task:
    task.complete = True
    task.save()

  else:
    raise HTTPException(status_code=404, detail=f"Task {id} not found.")

  return SUCCESS_RESPONSE


@router.post("/{id}")
async def dispatch(id: str, workflow_path: str):
  """Dispatch a Task to the next service.

  Args:
    id (str): unique id of the task

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the task is deleted
  """
  task = Task.find_by_id(id)
  workflow_path = ""

  workflow_steps = get_workflow_steps(task, workflow_path)
  service_url = get_service_url(workflow_steps)
  parameters = get_parameters(workflow_steps)

  # base_url = "http://classification-service/classification_service/v1/"\
  #   "classification/classification_api"
  # req_url = f"{base_url}?case_id={case_id}&uid={uid}" \
  #   f"&gcs_url={gcs_url}"

  response = requests.post(service_url, json=parameters)
  return response
