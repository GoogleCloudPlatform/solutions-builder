"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
