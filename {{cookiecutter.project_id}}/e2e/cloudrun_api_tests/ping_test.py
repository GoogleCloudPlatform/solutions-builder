import requests
from service_list import get_service_url


def test_api_ping():
  base_url = get_service_url("cloudrun-sample")
  if not base_url:
    raise NotFoundErr("Unable to locate the service URL for cloudrun-sample")

  res = requests.get(base_url + "/ping")
  assert res.status_code == 200


def test_hello_world():
  base_url = get_service_url("cloudrun-sample")
  if not base_url:
    raise NotFoundErr("Unable to locate the service URL for cloudrun-sample")

  res = requests.get(base_url + "/")
  assert res.text == "\"Hello World.\""
