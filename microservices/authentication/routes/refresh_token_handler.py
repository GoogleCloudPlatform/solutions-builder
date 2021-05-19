"""Class and methods for handling generate route."""
import json
from routes.base_handler import BaseHandler
from controllers.refresh_token_controller import generate_token
from middleware.validation import validate_request
from utils.exception_handler import InvalidRefreshTokenError


class RefreshTokenHandler(BaseHandler):
  """Class def handling routes."""

  @validate_request
  def post(self):
    """Method for post request."""
    try:
      return self.send_json(
          status=200,
          success=True,
          message="Token generated successfully",
          response=generate_token(json.loads(self.request.body)))
    except InvalidRefreshTokenError as err:
      return self.send_json(status=500, message=str(err), success=False)
