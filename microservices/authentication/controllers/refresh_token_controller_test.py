"""
    utility methods to execute unit tests for module refresh_token_controller.py
"""
import mock
import pytest
from controllers.refresh_token_controller import generate_token
from utils.exception_handler import InvalidRefreshTokenError

token_credentials = {
    "access_token": "eyJhbGciOiJSU........C7h4w",
    "expires_in": 3600,
    "token_type": "Bearer",
    "refresh_token": "AEu4IL2njCpop7p.......CU6sm8",
    "id_token": "eyJhbGciOiJSU.......G2rC7h4w",
    "user_id": "fiurc756IqcdRSs19upxiVLt1Gr2",
    "project_id": "test-project"
}


@mock.patch("controllers.refresh_token_controller.get_id_token")
def test_generate_token(mock_get_id_token):
  # arrange
  req_body = {"refresh_token": "ABC"}
  mock_get_id_token.return_value = token_credentials

  # action
  resp = generate_token(req_body)

  # assert
  assert resp == token_credentials


@mock.patch("controllers.refresh_token_controller.get_id_token")
def test_generate_token_invalid_refresh_token(mock_get_id_token):
  # arrange
  req_body = {"refresh_token": "ABC"}
  mock_get_id_token.return_value = {
      "error": {
          "message": "INVALID_REFRESH_TOKEN"
      }
  }

  # action
  with pytest.raises(InvalidRefreshTokenError) as err:
    generate_token(req_body)

  # assert
  assert str(err.value) == "INVALID_REFRESH_TOKEN"
