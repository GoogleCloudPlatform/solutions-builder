"""Methods for creating and returning a tornado web application."""
import tornado.web
from config import BASE_URL, BASE_URL_V2, SERVICE, IS_DEVELOPMENT

from routes.error_handler import ErrorHandler
from routes.main_handler import MainHandler
from routes.refresh_token_handler import RefreshTokenHandler
from routes.validate_token_handler import ValidateTokenHandler


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
  return tornado.web.Application([
      ("/ping", MainHandler), ("/ping/", MainHandler),
      ("/{service}/{version}/generate".format(**api_path), RefreshTokenHandler),
      ("/{service}/{version}/generate/".format(**api_path),
       RefreshTokenHandler),
      ("/{service}/{version}/validate".format(**api_path),
       ValidateTokenHandler),
      ("/{service}/{version}/validate/".format(**api_path),
       ValidateTokenHandler),
      ("/{service}/{version}/generate".format(**api_path_v2),
       RefreshTokenHandler),
      ("/{service}/{version}/generate/".format(**api_path_v2),
       RefreshTokenHandler),
      ("/{service}/{version}/validate".format(**api_path_v2),
       ValidateTokenHandler),
      ("/{service}/{version}/validate/".format(**api_path_v2),
       ValidateTokenHandler)
  ], **settings)
