from fastapi import APIRouter, HTTPException
from models.todo import Todo
import datetime

# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/todo", tags=["todo"])

SUCCESS_RESPONSE = {"status": "Success"}


@router.get("/{id}", response_model=Todo)
async def get(id: str):
  """Get a Todo

  Args:
    id (str): unique id of the todo

  Raises:
    HTTPException: 404 Not Found if todo doesn't exist for the given todo id
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [todo]: todo object for the provided todo id
  """
  todo = Todo.find_by_id(id)

  if todo is None:
    raise HTTPException(status_code=404, detail=f"Todo {id} not found.")
  return todo


@router.post("")
async def post(todo: Todo):
  """Create a Todo

  Args:
    data (Todo): Required body of the todo

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: todo ID of the todo if the todo is successfully created
  """
  try:
    existing_todo = Todo.find_by_id(todo.id)

    if existing_todo:
      raise HTTPException(status_code=409,
                          detail=f"Todo {todo.id} already exists.")
    todo.created_at = datetime.datetime.utcnow()
    todo.modified_at = datetime.datetime.utcnow()
    todo.save()
    return todo

  except Exception as e:
    raise HTTPException(status_code=500, detail=e) from e


@router.put("")
async def put(todo: Todo):
  """Update a Todo

  Args:
    data (Todo): Required body of the todo

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the todo is updated
  """
  existing_todo = Todo.find_by_id(todo.id)

  if existing_todo:
    todo.created_at = existing_todo.created_at
    todo.modified_at = datetime.datetime.utcnow()
    todo.save()

  else:
    raise HTTPException(status_code=404, detail=f"Todo {todo.id} not found.")

  return SUCCESS_RESPONSE


@router.delete("/{id}")
async def delete(id: str):
  """Delete a Todo

  Args:
    id (str): unique id of the todo

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the todo is deleted
  """

  todo = Todo.find_by_id(id)
  if todo is None:
    raise HTTPException(status_code=404, detail=f"Todo {id} not found.")

  todo.delete()

  return SUCCESS_RESPONSE
