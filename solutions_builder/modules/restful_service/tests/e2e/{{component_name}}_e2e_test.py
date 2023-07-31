import pytest, requests, time
from tests.e2e.e2e_utils import *


@pytest.fixture
def auth_token():
  return get_auth_identity_token()


@pytest.fixture
def service_url():
  service_url = exec_output(
      "gcloud run services describe {{resource_name}} --region=us-central1 --format='value(status.url)'"
  )
  return service_url.replace("\n", "")


def test_api_ping(auth_token, service_url):
  headers = {"Authorization": f"Bearer {auth_token}"}
  res = requests.get(service_url + "/ping", headers=headers)
  assert res.status_code == 200


def test_restful_create_get(auth_token, service_url):
  test_id = str(time.time())
  print(f"test_id = {test_id}")

  headers = {
      "Authorization": f"Bearer {auth_token}",
      "Accept": "application/json"
  }
  data = {
      "id": test_id,
      "title": "Title",
      "description": "Description",
      "status": "New",
  }

  # Create a new item
  url = service_url + f"/{{resource_name}}/{{data_model}}"
  res = requests.post(url, json=data, headers=headers)
  assert res.status_code == 200

  # Get the item by ID
  url = service_url + f"/{{resource_name}}/{{data_model}}/{test_id}"
  res = requests.get(url, headers=headers)
  assert res.status_code == 200

  # Verify the content
  res_data = res.json()
  assert res_data["id"] == test_id

  # Clean up
  url = service_url + f"/{{resource_name}}/{{data_model}}/{test_id}"
  res = requests.delete(url, headers=headers)
  assert res.status_code == 200

  # Verify if the item is deleted
  url = service_url + f"/{{resource_name}}/{{data_model}}/{test_id}"
  res = requests.get(url, headers=headers)
  assert res.status_code == 404


def test_restful_put_delete(auth_token, service_url):
  test_id = str(time.time())
  print(f"test_id = {test_id}")
  headers = {
      "Authorization": f"Bearer {auth_token}",
      "Accept": "application/json"
  }
  data = {
      "id": test_id,
      "title": "Title",
      "description": "Description",
      "status": "New",
  }

  # Create a new item
  url = service_url + f"/{{resource_name}}/{{data_model}}"
  res = requests.post(url, json=data, headers=headers)
  assert res.status_code == 200

  # Update the item by ID
  data = {
      "id": test_id,
      "title": "Updated Title",
      "description": "Updated description",
      "status": "In Progress",
  }
  url = service_url + f"/{{resource_name}}/{{data_model}}"
  res = requests.put(url, json=data, headers=headers)
  assert res.status_code == 200

  # Get the item by ID
  url = service_url + f"/{{resource_name}}/{{data_model}}/{test_id}"
  print(f"url = {url}")
  res = requests.get(url, headers=headers)
  assert res.status_code == 200

  # Verify the content
  res_data = res.json()
  assert res_data["id"] == test_id
  assert res_data["title"] == "Updated Title"
  assert res_data["description"] == "Updated description"
  assert res_data["status"] == "In Progress"

  # Clean up
  url = service_url + f"/{{resource_name}}/{{data_model}}/{test_id}"
  res = requests.delete(url, headers=headers)
  assert res.status_code == 200

  # Verify if the item is deleted
  url = service_url + f"/{{resource_name}}/{{data_model}}/{test_id}"
  res = requests.get(url, headers=headers)
  assert res.status_code == 404
