"""
Copyright 2023 Google LLC

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

import pytest
from .vars import *

def test_replace_var_to_template():
  # Test with equals and quotes
  text = "project_id = \"not-replaced-yet\" # sb-var:project_id"
  text = replace_var_to_template("project_id", text)
  assert text == "project_id = \"{{project_id}}\" # sb-var:project_id"

  # Test with equals without quotes
  text = "project_id = test # sb-var:project_id"
  text = replace_var_to_template("project_id", text)
  assert text == "project_id = {{project_id}} # sb-var:project_id"

  # Test with comma without quotes
  text = "project_id: test # sb-var:project_id"
  text = replace_var_to_template("project_id", text)
  assert text == "project_id: {{project_id}} # sb-var:project_id"

def test_replace_var_to_custom_template():
  # Test with equals and quotes
  text = "project_id = \"not-replaced-yet\" # sb-var:project_id:prefix-{{project_id}}-suffix"
  text = replace_var_to_template("project_id", text, custom_template=True)
  assert text == "project_id = \"prefix-{{project_id}}-suffix\" # sb-var:project_id:prefix-{{project_id}}-suffix"

def test_replace_var_to_value():
  text = "project_id = \"not-replaced-yet\" # sb-var:project_id"
  text = replace_var_to_value("project_id", "fake-id", text)
  assert text == "project_id = \"fake-id\" # sb-var:project_id"

  text = "  PROJECT_ID: not-replaced-yet # sb-var:project_id"
  text = replace_var_to_value("project_id", "fake-id", text)
  assert text == "  PROJECT_ID: fake-id # sb-var:project_id"

def test_replace_with_multiple_lines():
  text = """
    env:
      PROJECT_ID: not-replaced-yet # sb-var:project_id
    """
  text = replace_var_to_value("project_id", "fake-id", text)

  print(text)
  assert text == """
    env:
      PROJECT_ID: fake-id # sb-var:project_id
    """

def test_replace_var_to_value_custom_template():
  text = "project_id = \"not-replaced-yet\" # sb-var:project_id:prefix-{{project_id}}-suffix"
  text = replace_var_to_value("project_id", "fake-id", text)
  assert text == "project_id = \"prefix-fake-id-suffix\" # sb-var:project_id:prefix-{{project_id}}-suffix"
