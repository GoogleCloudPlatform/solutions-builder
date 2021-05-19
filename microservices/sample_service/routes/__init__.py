"""Methods for creating and returning a tornado web application."""
import tornado.web
from config import SERVICE, BASE_URL, BASE_URL_V2, IS_DEVELOPMENT
from routes.error_handler import ErrorHandler
from routes.main_handler import MainHandler


def make_app():
  """
        Create a tornado web application.
        Args:
            None
        Returns:
            tornado web application
    """
  settings = {"default_handler_class": ErrorHandler, "debug": IS_DEVELOPMENT}
  api_path = {"service": SERVICE, "version": BASE_URL}
  api_path_v2 = {"service": SERVICE, "version": BASE_URL_V2}
  return tornado.web.Application(
      [("/ping", MainHandler), ("/ping/", MainHandler)], **settings)
