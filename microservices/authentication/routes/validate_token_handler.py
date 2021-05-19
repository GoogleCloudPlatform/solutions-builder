"""Class and methods for handling validate route."""

from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError
from routes.base_handler import BaseHandler
from controllers.validate_token_controller import validate_token


class ValidateTokenHandler(BaseHandler):
  """Class def handling routes."""

  def get(self):
    """Method for get request"""
    try:
      if "Authorization" in self.request.headers and \
              self.request.headers["Authorization"] and \
              len(self.request.headers["Authorization"].split(" ")) == 2:
        return self.send_json(
            response=validate_token(self.request.headers["Authorization"]))
      return self.send_json(
          status=403, message=str("TOKEN_NOT_FOUND"), success=False)

    except (InvalidIdTokenError, ExpiredIdTokenError) as err:
      return self.send_json(status=401, message=str(err), success=False)
