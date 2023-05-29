from fastapi import APIRouter, HTTPException
from models.{{data_model}} import {{data_model | capitalize}}
import datetime

# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/{{data_model}}", tags=["{{data_model}}"])

SUCCESS_RESPONSE = {"status": "Success"}


@router.get("/{id}", response_model={{data_model | capitalize}})
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
async def post({{data_model}}: {{data_model | capitalize}}):
  """Create a {{data_model | capitalize}}

  Args:
    data ({{data_model | capitalize}}): Required body of the {{data_model}}

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {{data_model}} ID of the {{data_model}} if the {{data_model}} is successfully created
  """
  try:
    id = {{data_model}}.id
    existing_{{data_model}} = {{data_model | capitalize}}.find_by_id(id)

    if existing_{{data_model}}:
      raise HTTPException(status_code=409,
                          detail=f"{{data_model | capitalize}} {id} already exists.")
    {{data_model}}.created_at = datetime.datetime.utcnow()
    {{data_model}}.modified_at = datetime.datetime.utcnow()
    {{data_model}}.save()
    return {{data_model}}

  except Exception as e:
    raise HTTPException(status_code=500, detail=e) from e


@router.put("")
async def put({{data_model}}: {{data_model | capitalize}}):
  """Update a {{data_model | capitalize}}

  Args:
    data ({{data_model | capitalize}}): Required body of the {{data_model}}

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the {{data_model}} is updated
  """
  id = {{data_model}}.id
  existing_{{data_model}} = {{data_model | capitalize}}.find_by_id(d)

  if existing_{{data_model}}:
    {{data_model}}.created_at = existing_{{data_model}}.created_at
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

  {{data_model}}.delete()

  return SUCCESS_RESPONSE
