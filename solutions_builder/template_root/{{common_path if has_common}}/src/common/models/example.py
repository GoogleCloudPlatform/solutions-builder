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
"""
Data model for example list.
"""

import os

from firedantic import Model
from firedantic.exceptions import ModelNotFoundError
from datetime import datetime

# GCP project_id from system's environment variable.
PROJECT_ID = os.environ.get("PROJECT_ID", "")

# Database prefix for integration and e2e test purpose.
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")


# Firebase data model in "examples" collection.
class Example(Model):
  """Example ORM class"""
  __collection__ = "examples"

  id: str = "1234"
  title: str = "Title"
  description: str = "Description"
  is_done: bool = False
  created_at: datetime
  modified_at: datetime = None

  @classmethod
  def find_by_id(cls, id):
    try:
      example = Example.get_by_doc_id(id)
    except ModelNotFoundError:
      return None

    return example
