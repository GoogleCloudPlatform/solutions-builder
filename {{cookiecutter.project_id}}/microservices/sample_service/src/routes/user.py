""" User endpoints """
import datetime
from fastapi import APIRouter, HTTPException
from schemas.user import UserModel
from common.models import User
from common.utils.logging_handler import Logger

# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/user", tags=["User"])

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


@router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
  """Get a user

  Args:
    user_id (str): unique id of the user

  Raises:
    HTTPException: 404 Not Found if user doesn't exist for the given user id
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [user]: user object for the provided user id
  """
  user = User.find_by_user_id(user_id)

  if user is None:
    raise HTTPException(status_code=404, detail="user not found")
  return user


@router.post("")
async def create_user(input_user: UserModel):
  """Register a user

  Args:
    input_user (UserModel): Required body of the user

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: user ID of the user if the user is successfully created,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    new_user = User()
    input_user_dict = {**input_user.dict()}
    new_user = new_user.from_dict(input_user_dict)
    existing_user = User.find_by_user_id(input_user_dict["user_id"])
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

    if existing_user is None:
      new_user.created_timestamp = timestamp
      new_user.last_updated_timestamp = timestamp
      new_user.save()
    else:
      new_user.last_updated_timestamp = timestamp
      new_user.update.update(existing_user.id)

    return new_user.user_id

  except Exception as e:
    Logger.error(e)
    raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("")
async def update_user(input_user: UserModel):
  """Update a user

  Args:
    input_user (UserModel): Required body of the user

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the user is updated,
    {'status': 'Failed'} if the user updation raises an exception
  """
  user = User()
  input_user_dict = {**input_user.dict()}
  user = user.from_dict(input_user_dict)
  existing_user = User.find_by_user_id(input_user_dict["user_id"])

  timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

  if existing_user:
    try:
      user.last_updated_timestamp = timestamp
      user.update(existing_user.id)

    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e)) from e

  else:
    raise HTTPException(status_code=404, detail="user not found")

  return SUCCESS_RESPONSE


@router.delete("/{user_id}")
async def delete_user(user_id: str):
  """Delete a user

  Args:
    user_id (str): unique id of the user

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the user is deleted,
    {'status': 'Failed'} if the user deletion raises an exception
  """

  user = User.find_by_user_id(user_id)
  if user is None:
    raise HTTPException(status_code=404, detail="user not found")

  User.collection.delete(user.key)

  return SUCCESS_RESPONSE
