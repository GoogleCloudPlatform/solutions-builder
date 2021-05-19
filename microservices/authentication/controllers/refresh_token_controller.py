"""Utility method for handling token generation."""
from config import API_KEY
from services.refresh_token_service import get_id_token
from utils.exception_handler import InvalidRefreshTokenError


def generate_token(req_body):
  """
          Calls get_id_token method from refresh_token_service
          and Returns Response or Error.
          Args:
              req_body: Dict
          Returns
              token_credentials: Dict
      """

  payload = "grant_type=refresh_token&refresh_token={}".format(
      req_body["refresh_token"])
  response = get_id_token(payload, API_KEY)
  if "error" in response:
    raise InvalidRefreshTokenError(response["error"]["message"])
  return response
