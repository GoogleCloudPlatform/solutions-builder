from xml.dom import NotFoundErr
import requests
from endpoint_proxy import get_baseurl


def test_api_ping():
  base_url = get_baseurl("user-service")
  if not base_url:
    raise NotFoundErr("Unable to locate the service URL for user-service")
  res = requests.get(base_url + "/ping")
  assert res.status_code == 200


def test_hello_world():
  base_url = get_baseurl("user-service")
  if not base_url:
    raise NotFoundErr("Unable to locate the service URL for user-service")
  res = requests.get(base_url + "/")
  assert "You've reached the Sample Service" in res.text
