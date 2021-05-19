"""Utility methods for validation of authentication."""
import firebase_admin
from firebase_admin import auth

default_app = firebase_admin.initialize_app()


def verify_token(token):
  """
          Verifies id token issued to user, Return user authentication
          details is token is valid, else Returns token expired as error
          Args:
              Id Token: String
          Returns:
              User auth details: Dict
      """
  return auth.verify_id_token(token)
