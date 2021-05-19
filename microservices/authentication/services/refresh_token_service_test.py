"""
    utility methods to execute unit tests for module refresh_token_service.py
"""
import mock
from services.refresh_token_service import get_id_token

token_credentials = {
    "access_token": "eyJhbGciOiJSU........C7h4w",
    "expires_in": 3600,
    "token_type": "Bearer",
    "refresh_token": "AEu4IL2njCpop7p.......CU6sm8",
    "id_token": "eyJhbGciOiJSU.......G2rC7h4w",
    "user_id": "fiurc756IqcdRSs19upxiVLt1Gr2",
    "project_id": "test-project"
}


def mocked_requests_post(*args, **kwargs):

  class MockResponse:

    def __init__(self, json_data, status_code):
      self.json_data = json_data
      self.status_code = status_code

    def json(self):
      return self.json_data

  if args[
      0] == "https://securetoken.googleapis.com/v1/token" and "key" in kwargs[
          "params"]:
    return MockResponse(token_credentials, 200)

  return MockResponse(None, 404)


@mock.patch("services.refresh_token_service.requests.post")
def test_get_id_token(mock_post):
  # arrange
  refresh_token = "ABC"
  payload = "grant_type=refresh_token&refresh_token={}".format(refresh_token)
  api_key = "AIzaSyDMntfoVTtoGknSdqqMcGy5E-GsDuyjx0M"
  mock_post.side_effect = mocked_requests_post
  # action
  resp = get_id_token(payload, api_key)

  # assert
  print(resp)
  assert resp is not None
  assert "id_token" in resp
  assert resp == token_credentials
