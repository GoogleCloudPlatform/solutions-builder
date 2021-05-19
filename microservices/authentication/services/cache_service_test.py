"""
    utility methods to execute unit tests for module cache_service.py
"""
import mock
import json
from services.cache_service import set_key, get_key

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
        "fiurc756IqcdRSs19upxiVLt1Gr2",
    "new_user":
        True
}
user_id = "fiurc756IqcdRSs19upxiVLt1Gr2"
test_user = {"email": "test.user@gmail.com", "name": "Test User"}


@mock.patch("services.cache_service.r.set")
def test_set_key(mock_set):
  # arrange
  mock_set.return_value = True

  # action
  cache_status = set_key("cache::{}".format(user_id), test_user)

  # assert
  assert cache_status is True


@mock.patch("services.cache_service.r.set")
def test_set_key_with_expiry(mock_set):

  mock_set.return_value = True
  cache_status = set_key("cache::token", auth_details, 1800)
  # assert
  assert cache_status


@mock.patch("services.cache_service.r.get")
def test_get_key(mock_get):
  # arrange
  mock_get.return_value = json.dumps(test_user).encode("utf-8")

  # action
  cached_value = get_key("cache::{}".format(user_id))

  # assert
  assert cached_value == test_user


@mock.patch("services.cache_service.r.get")
def test_get_key_with_expiry(mock_get):
  # arrange
  mock_get.return_value = json.dumps(auth_details).encode("utf-8")

  # action
  cached_value = get_key("cache::token")

  # assert
  assert cached_value == auth_details
