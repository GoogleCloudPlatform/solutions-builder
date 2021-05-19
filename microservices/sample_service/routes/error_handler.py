"""Class and methods for handling errors."""
from routes.base_handler import BaseHandler


class ErrorHandler(BaseHandler):
  """Class def for handling errors."""

  def prepare(self):
    """Method for error response."""
    return self.send_json(
        message="The resource you are looking for is not found",
        status=404,
        success=False)
