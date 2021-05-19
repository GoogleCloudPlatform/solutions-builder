"""Classes for custom exception handling"""


class Error(Exception):
  """Base class for other exceptions"""


class InvalidRefreshTokenError(Error):
  """Raised when the refresh token is invalid"""


class ExpiredRefreshTokenError(Error):
  """Raised when the refresh token is expired"""
