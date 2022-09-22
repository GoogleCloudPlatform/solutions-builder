import json
import os

SERVICE_NAME_PREFIX =  os.getenv("SERVICE_NAME_PREFIX", "")
SERVICE_LIST_JSON = os.getenv("SERVICE_LIST_JSON")
assert SERVICE_LIST_JSON

service_list = []
with open(SERVICE_LIST_JSON, "r") as json_file:
  service_list = json.load(json_file)

def get_service_url(service_name):
  for item in service_list:
    if item["metadata"]["name"] == f"{SERVICE_NAME_PREFIX}{service_name}":
      return item["status"]["address"]["url"]
  return None
