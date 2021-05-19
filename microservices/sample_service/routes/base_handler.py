"""Class and methods for handling base operations."""
import json
from tornado import web


class BaseHandler(web.RequestHandler):
  """Base Class def."""
  user_email = None

  def set_default_headers(self):
    """Set default headers."""
    self.set_header("Content-type", "application/json")
    self.set_header(
        "Access-Control-Allow-Headers",
        "Content-Type, Access-Control-Allow-Origin, \
                            Access-Control-Allow-Headers, X-Requested-By, \
                                Access-Control-Allow-Methods")

  def send_json(self, message="", success=True, response=None, status=200):
    """
            Return dictionary as response.
            Args:
                Dictionary containing:
                    "success" - True or False
                    "message" - "success message" or error message
                    "data" - dictionary containing response
                            from inference
        """
    self.set_status(status)
    return self.write(
        json.dumps({
            "success": success,
            "message": message,
            "data": response
        }))
