"""
  Tests for User endpoints
"""
import os
import json
import datetime

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.testing.client_with_emulator import client_with_emulator

from common.models import User
import mock

# assigning url
API_URL = "http://localhost/sample_service"
TEST_USER = {
    "user_id": "user-12345",
    "first_name": "John",
    "middle_name": "A",
    "last_name": "Marshal",
    "date_of_birth": "1994-09-10",
    "email_address": "john.338@gmail.com",
}

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def test_get_user(client_with_emulator):
  user_dict = TEST_USER
  user = User.from_dict(user_dict)
  user.save()

  url = API_URL + f"/user/{user.user_id}"
  data = TEST_USER
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)

  assert resp.status_code == 200, "Status 200"
  assert json_response == data, "Return data doesn't match."


def test_get_nonexist_user(client_with_emulator):
  user_id = "non_exist_user_id"
  url = API_URL + f"/user/{user_id}"
  data = {"detail": "user not found"}
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Return data doesn't match."


def test_post_user_new(client_with_emulator):
  input_user = TEST_USER
  url = API_URL + "/user"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.post(url, json=input_user)

  assert resp.status_code == 200, "Status 200"

  # now see if GET endpoint returns same data
  url = API_URL + f"/user/{input_user['user_id']}"
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert json_response == input_user

  # now check and confirm it is properly in the databse
  loaded_user = User.find_by_user_id(input_user["user_id"])
  loaded_user_dict = loaded_user.to_dict()

  # popping id and key for equivalency test
  loaded_user_dict.pop("id")
  loaded_user_dict.pop("key")

  timestamp = datetime.datetime.utcnow()

  # remove the timestamps since they aren't returned in the API
  # response doesn't include
  acceptable_sec_diff = 15
  created_timestamp = datetime.datetime.strptime(
      loaded_user_dict.pop("created_timestamp"), "%Y-%m-%d %H:%M:%S.%f")
  last_updated_timestamp = datetime.datetime.strptime(
      loaded_user_dict.pop("last_updated_timestamp"), "%Y-%m-%d %H:%M:%S.%f")

  assert (timestamp - created_timestamp).total_seconds() < acceptable_sec_diff
  assert (timestamp -
          last_updated_timestamp).total_seconds() < acceptable_sec_diff

  # assert that rest of the fields are equivalent
  assert loaded_user_dict == input_user


def test_put_user(client_with_emulator):
  # create new user with POST to get timestamps
  input_user = TEST_USER
  url = API_URL + "/user"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.post(url, json=input_user)

  # modify user
  input_user["first_name"] = "Emmy"

  url = API_URL + "/user"
  resp_data = SUCCESS_RESPONSE
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.put(url, json=input_user)

  json_response = json.loads(resp.text)
  assert resp.status_code == 200, "Status 200"
  assert json_response == resp_data, "Response received"

  # now make sure user is updated and updated_timestamp is changed
  url = API_URL + f"/user/{input_user['user_id']}"
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)

  assert json_response == input_user

  # assert timestamp has been updated
  # loading from DB since not surfaced in API
  loaded_user = User.find_by_user_id(input_user["user_id"])

  created_timestamp = datetime.datetime.strptime(loaded_user.created_timestamp,
                                                 "%Y-%m-%d %H:%M:%S.%f")
  last_updated_timestamp = datetime.datetime.strptime(
      loaded_user.last_updated_timestamp, "%Y-%m-%d %H:%M:%S.%f")

  assert created_timestamp < last_updated_timestamp


def test_put_user_negative(client_with_emulator):
  user_dict = TEST_USER
  user = User.from_dict(user_dict)
  user.save()

  input_user = TEST_USER
  input_user["user_id"] = "U2DDBkl3Ayg0PWudzhI"

  url = API_URL + "/user"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.put(url, json=input_user)

  assert resp.status_code == 404, "Status 404"


def test_delete_user(client_with_emulator):
  user_dict = TEST_USER
  user = User.from_dict(user_dict)
  user.save()

  # confirm in backend with API
  url = API_URL + f"/user/{user.user_id}"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200, "Status 200"

  # now delete user with API
  url = API_URL + f"/user/{user.user_id}"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.delete(url)

  assert resp.status_code == 200, "Status 200"

  # now confirm user gone with API
  url = API_URL + f"/user/{user.user_id}"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 404, "Status 404"


def test_delete_user_negative(client_with_emulator):
  user_dict = TEST_USER
  user = User.from_dict(user_dict)
  user.save()

  url = API_URL + "/user/U2DDBkl3Ayg0PWudzhIi"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.delete(url)

  data = {"detail": "user not found"}
  resp = client_with_emulator.delete(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"
