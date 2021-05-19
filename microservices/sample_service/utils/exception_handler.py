"""Classes for custom exception handling"""


class Error(Exception):
  """Base class for other exceptions"""


class InvalidTokenError(Error):
  "Raised when an invalid token is passed"


class InvalidContextError(Error):
  """Raised when the context passed is invalid"""


class InvalidSessionIdError(Error):
  """Raised when the session id passed is invalid"""


class InternalServerError(Error):
  """Raised when an error due to code occurs"""
