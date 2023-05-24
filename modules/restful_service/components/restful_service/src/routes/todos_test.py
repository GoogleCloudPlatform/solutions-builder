"""
  Tests for User endpoints
"""
import os
import json
import datetime

from models import Todo
import mock

# assigning url
API_URL = "http://localhost/restful_service"
TEST_TODO = {
    "id": "todo-12345",
    "title": "Title",
    "description": "Description",
    "is_done": False,
}
FIRESTORE_EMULATOR_PORT = "9000"
os.environ["FIRESTORE_EMULATOR_HOST"] = f"localhost:{FIRESTORE_EMULATOR_PORT}"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def test_get_todo(client_with_emulator):
  todo = Todo.parse_obj(TEST_TODO)
  todo.save()

  url = API_URL + f"/todo/{todo.id}"
  data = TEST_TODO
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)

  assert resp.status_code == 200, "Status 200"
  assert json_response == data, "Return data doesn't match."


def test_get_nonexist_todo(client_with_emulator):
  todo_id = "non_exist_todo_id"
  url = API_URL + f"/todo/{todo_id}"
  data = {"detail": "user not found"}
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Return data doesn't match."


def test_post_user_new(client_with_emulator):
  input_todo = TEST_TODO
  url = API_URL + "/user"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.post(url, json=input_todo)

  assert resp.status_code == 200, "Status 200"

  # now see if GET endpoint returns same data
  url = API_URL + f"/todo/{input_todo['todo_id']}"
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert json_response == input_todo

  # now check and confirm it is properly in the databse
  loaded_todo = User.find_by_todo_id(input_todo["todo_id"])
  loaded_user_dict = loaded_todo.to_dict()

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
  assert loaded_user_dict == input_todo


def test_put_todo(client_with_emulator):
  # create new user with POST to get timestamps
  input_todo = TEST_TODO
  url = API_URL + "/user"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.post(url, json=input_todo)

  # modify user
  input_todo["first_name"] = "Emmy"

  url = API_URL + "/user"
  resp_data = SUCCESS_RESPONSE
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.put(url, json=input_todo)

  json_response = json.loads(resp.text)
  assert resp.status_code == 200, "Status 200"
  assert json_response == resp_data, "Response received"

  # now make sure user is updated and updated_timestamp is changed
  url = API_URL + f"/todo/{input_todo['todo_id']}"
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)

  assert json_response == input_todo

  # assert timestamp has been updated
  # loading from DB since not surfaced in API
  loaded_todo = User.find_by_todo_id(input_todo["todo_id"])

  created_timestamp = datetime.datetime.strptime(loaded_user.created_timestamp,
                                                 "%Y-%m-%d %H:%M:%S.%f")
  last_updated_timestamp = datetime.datetime.strptime(
      loaded_user.last_updated_timestamp, "%Y-%m-%d %H:%M:%S.%f")

  assert created_timestamp < last_updated_timestamp


def test_put_user_negative(client_with_emulator):
  user_dict = TEST_TODO
  todo = Todo.parse_obj(user_dict)
  todo.save()

  input_todo = TEST_TODO
  input_todo["todo_id"] = "U2DDBkl3Ayg0PWudzhI"

  url = API_URL + "/user"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.put(url, json=input_todo)

  assert resp.status_code == 404, "Status 404"


def test_delete_todo(client_with_emulator):
  user_dict = TEST_TODO
  todo = Todo.parse_obj(user_dict)
  todo.save()

  # confirm in backend with API
  url = API_URL + f"/todo/{todo.id}"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200, "Status 200"

  # now delete user with API
  url = API_URL + f"/todo/{todo.id}"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.delete(url)

  assert resp.status_code == 200, "Status 200"

  # now confirm user gone with API
  url = API_URL + f"/todo/{todo.id}"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 404, "Status 404"


def test_delete_user_negative(client_with_emulator):
  user_dict = TEST_TODO
  todo = Todo.parse_obj(user_dict)
  todo.save()

  url = API_URL + "/todo/U2DDBkl3Ayg0PWudzhIi"
  with mock.patch("routes.user.Logger"):
    resp = client_with_emulator.delete(url)

  data = {"detail": "user not found"}
  resp = client_with_emulator.delete(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"
