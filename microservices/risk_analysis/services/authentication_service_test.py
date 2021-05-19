"""
    utility methods to execute unit tests for module authentication_service.py
"""
import mock
from config import SERVICES
from services.authentication_service import get_auth_service_response

host = SERVICES["authentication"]["host"]
port = SERVICES["authentication"]["port"]

user_details = {
    "name": "Test User",
    "email": "test.user@gmail.com",
    "user_id": "fibUythnoin98Udeslo"
}


def mocked_requests_get(**kwargs):

  class MockResponse:

    def __init__(self, json_data, status_code):
      self.json_data = json_data
      self.status_code = status_code

    def json(self):
      return self.json_data

  if kwargs["url"] == "http://{}:{}/authentication/api/v1/validate".format(
      host, port):
    return MockResponse(user_details, 200)
  elif kwargs["url"] == "http://{}:{}/authentication/api/v2/validate".format(
      host, port):
    return MockResponse(user_details, 200)

  return MockResponse(None, 404)


@mock.patch(
    "services.authentication_service.requests.get",
    side_effect=mocked_requests_get)
def test_get_auth_service_response(mock_get):
  # arrange
  token = "Bearer xyz"

  # action
  resp = get_auth_service_response(token)

  # assert
  assert resp == user_details
  assert len(mock_get.call_args) == 2
  mock_get.assert_called_once_with(
      url="http://{}:{}/authentication/api/v2/validate".format(host, port),
      headers={
          "Content-Type": "application/json",
          "Authorization": token
      })
