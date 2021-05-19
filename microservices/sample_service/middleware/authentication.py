"""Utility method to validate user based on Id Token"""
from services.authentication_service import get_auth_service_response
from utils.logging_handler import Logger
from utils.exception_handler import InvalidTokenError


def verify_authentication(func):
  """
          This decorator function validates Id token passed
          in Authorization headers and Returns to calling function.
          Throws error if token validation fails.
          Args:
              func
          Returns:
              func or raise error
      """

  async def verify(*args, **kwargs):
    Logger.info("Within Authentication Decorator")
    try:
      if "Authorization" in args[0].request.headers and \
              args[0].request.headers["Authorization"]:
        token = args[0].request.headers["Authorization"]
      else:
        Logger.error("Token not Found")
        return args[0].send_json(
            status=403, message=str("TOKEN_NOT_FOUND"), success=False)
      resp = get_auth_service_response(token)
      if resp["success"] is False:
        Logger.error(resp["message"])
        raise InvalidTokenError(resp["message"])
      args[0].user_email = resp["data"]["email"]
      args[0].user_id = resp["data"]["user_id"]
      await func(*args, **kwargs)
    except InvalidTokenError as err:
      return args[0].send_json(status=401, message=str(err), success=False)

  return verify


def verify_auth_sync(func):
  """
          This decorator function validates Id token passed
          in Authorization headers and Returns to calling function.
          Throws error if token validation fails.
          Args:
              func
          Returns:
              func or raise error
      """

  def verify(*args, **kwargs):
    Logger.info("Within Authentication Decorator")
    try:
      if "Authorization" in args[0].request.headers and \
              args[0].request.headers["Authorization"]:
        token = args[0].request.headers["Authorization"]
      else:
        Logger.error("Token not Found")
        return args[0].send_json(
            status=403, message=str("TOKEN_NOT_FOUND"), success=False)
      resp = get_auth_service_response(token)
      if resp["success"] is False:
        Logger.error(resp["message"])
        raise InvalidTokenError(resp["message"])
      args[0].user_email = resp["data"]["email"]
      args[0].user_id = resp["data"]["user_id"]
      func(*args, **kwargs)
    except InvalidTokenError as err:
      return args[0].send_json(status=401, message=str(err), success=False)

  return verify
