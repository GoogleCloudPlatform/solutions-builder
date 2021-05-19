"""
utility methods to execute unit tests for module validate_token_controller.py
"""
import mock
from controllers.validate_token_controller import (handle_user, validate_token)

auth_details = {
    "name":
        "Test User",
    "picture":
        "https://lh3.googleusercontent.com/-I8CTmvNmtLE\
      /AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rdBqybASKV35NeQTu_cEL5eTO5G9w/photo.jpg",
    "iss":
        "https://securetoken.google.com/my-dummy-project",
    "aud":
        "my-dummy-project",
    "auth_time":
        1579875095,
    "user_id":
        "fiurc756IqcdRSs19upxiVLt1Gr2",
    "sub":
        "fiurc756IqcdRSs19upxiVLt1Gr2",
    "iat":
        1579875097,
    "exp":
        1579878697,
    "email":
        "test.user@gmail.com",
    "email_verified":
        True,
    "firebase": {
        "identities": {
            "google.com": [104415576250754890000],
            "microsoft.com": ["96d7dbe4-0abf-495c-bd1d-cab8af465ac4"],
            "email": ["test.user@gmail.com"]
        },
        "sign_in_provider": "google.com"
    },
    "uid":
        "fiurc756IqcdRSs19upxiVLt1Gr2"
}


@mock.patch("controllers.validate_token_controller.set_key")
@mock.patch("controllers.validate_token_controller.user_exist")
def test_handle_user(mock_user_exist, mock_set_key):
  # arrange
  decoded_token = {
      "email": "test.user@gmail.com",
      "name": "Test User",
      "user_id": "fiurc756IqcdRSs19upxiVLt1Gr2"
  }
  mock_user_exist.return_value = True
  mock_set_key.return_value = True

  # action
  user_type = handle_user(decoded_token)

  # assert
  assert "new_user" in user_type
  assert user_type["new_user"] is False


@mock.patch("controllers.validate_token_controller.set_key")
@mock.patch("controllers.validate_token_controller.insert_document")
@mock.patch("controllers.validate_token_controller.user_exist")
def test_handle_new_user(mock_user_exist, mock_insert_document, mock_set_key):
  # arrange
  decoded_token = {
      "email": "test1.user@gmail.com",
      "name": "Test1 User",
      "user_id": "luk9GfcvxWuiopqaXepqY"
  }
  mock_user_exist.return_value = False
  mock_insert_document.return_value = mock.Mock(
      id=decoded_token["user_id"], data=decoded_token)
  mock_set_key.return_value = True

  # action
  user_type = handle_user(decoded_token)

  # assert
  assert "new_user" in user_type
  assert user_type["new_user"] is True


@mock.patch("controllers.validate_token_controller.handle_user")
@mock.patch("controllers.validate_token_controller.set_key")
@mock.patch("controllers.validate_token_controller.verify_token")
@mock.patch("controllers.validate_token_controller.get_key")
def test_validate_token(mock_get_key, mock_verify_token, mock_set_key,
                        mock_handle_user):
  # arrange
  bearer_token = "Bearer XYZ"
  mock_get_key.return_value = None
  mock_verify_token.return_value = auth_details
  mock_set_key.return_value = True
  mock_handle_user.return_value = {"new_user": True}

  # action
  result = validate_token(bearer_token)

  # assert
  assert result is not None
  assert "new_user" in result
  assert result["name"] == auth_details["name"]
  assert result["email"] == auth_details["email"]
  assert result["user_id"] == auth_details["user_id"]


@mock.patch("controllers.validate_token_controller.get_key")
def test_validate_token_cached(mock_get_key):
  # arrange
  bearer_token = "Bearer PQR"
  mock_get_key.return_value = auth_details

  # action
  result = validate_token(bearer_token)

  # assert
  assert result is not None
  assert "new_user" in result
  assert result["name"] == auth_details["name"]
  assert result["email"] == auth_details["email"]
  assert result["user_id"] == auth_details["user_id"]
