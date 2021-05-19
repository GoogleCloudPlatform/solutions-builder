"""Class and methods for handling connection related operatios."""
from routes.base_handler import BaseHandler


class MainHandler(BaseHandler):
  """Main Class def."""

  def get(self):
    """Method for connection check."""
    return self.send_json(
        message="You have Successfully reached Authentication API")
