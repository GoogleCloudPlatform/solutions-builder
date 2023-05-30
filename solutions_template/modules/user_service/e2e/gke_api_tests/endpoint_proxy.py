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

import yaml

port_config_data = []
with open("e2e/utils/port_config.yaml", "r") as stream:
  port_config = yaml.safe_load(stream)
  port_config_data = port_config.get("data", [])


def get_baseurl(service_name):
  port = port_config_data[service_name + ".PORT"].split(":")[0]
  return f"http://localhost:{port}"
