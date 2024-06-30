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

from fastapi import APIRouter, HTTPException
from models.{{data_model}} import {{data_model | capitalize}}
from schemas.{{data_model}} import {{data_model | capitalize}}Schema
import datetime

# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/{{data_model}}", tags=["{{data_model}}"])

SUCCESS_RESPONSE = {"status": "Success"}


@router.get("/{id}", response_model={{data_model | capitalize}}Schema)
async def get(id: str):
  """Get a {{data_model | capitalize}}

  Args:
    id (str): unique id of the {{data_model}}

  Raises:
    HTTPException: 404 Not Found if {{data_model}} doesn't exist for the given {{data_model}} id
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [{{data_model}}]: {{data_model}} object for the provided {{data_model}} id
  """
  {{data_model}} = {{data_model | capitalize}}.find_by_id(id)

  if {{data_model}} is None:
    raise HTTPException(status_code=404, detail=f"{{data_model | capitalize}} {id} not found.")
  return {{data_model}}


@router.post("")
async def post(data: {{data_model | capitalize}}Schema):
  """Create a {{data_model | capitalize}}

  Args:
    data ({{data_model | capitalize}}): Required body of the {{data_model}}

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {{data_model}} ID of the {{data_model}} if the {{data_model}} is successfully created
  """
  id = data.id
  existing_{{data_model}} = {{data_model | capitalize}}.find_by_id(id)

  if existing_{{data_model}}:
    raise HTTPException(status_code=409,
                        detail=f"{{data_model | capitalize}} {id} already exists.")

  new_{{data_model}} = {{data_model | capitalize}}()
  new_{{data_model}} = new_{{data_model}}.from_dict({**data.dict()})
  new_{{data_model}}.created_at = datetime.datetime.utcnow()
  new_{{data_model}}.modified_at = datetime.datetime.utcnow()
  new_{{data_model}}.save()

  return SUCCESS_RESPONSE


@router.put("")
async def put(data: {{data_model | capitalize}}Schema):
  """Update a {{data_model | capitalize}}

  Args:
    data ({{data_model | capitalize}}): Required body of the {{data_model}}

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the {{data_model}} is updated
  """
  id = data.id
  {{data_model}} = {{data_model | capitalize}}.find_by_id(id)

  if {{data_model}}:
    {{data_model}} = {{data_model}}.from_dict({**data.dict()})
    {{data_model}}.modified_at = datetime.datetime.utcnow()
    {{data_model}}.save()

  else:
    raise HTTPException(status_code=404, detail=f"{{data_model | capitalize}} {id} not found.")

  return SUCCESS_RESPONSE


@router.delete("/{id}")
async def delete(id: str):
  """Delete a {{data_model | capitalize}}

  Args:
    id (str): unique id of the {{data_model}}

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the {{data_model}} is deleted
  """

  {{data_model}} = {{data_model | capitalize}}.find_by_id(id)
  if {{data_model}} is None:
    raise HTTPException(status_code=404, detail=f"{{data_model | capitalize}} {id} not found.")

  {{data_model | capitalize}}.collection.delete({{data_model}}.key)

  return SUCCESS_RESPONSE
