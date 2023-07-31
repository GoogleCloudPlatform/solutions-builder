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
Data model for Task. See https://octabyte.io/FireO/ for details.
"""

import os

from fireo.models import Model
from fireo.fields import IDField, TextField, TextField, BooleanField, Field
from fireo.queries.errors import ReferenceDocNotExist
from datetime import datetime
from enum import Enum
from config import PROJECT_ID, DATABASE_PREFIX


class TaskStatus(Enum):
  NEW = "new"
  IN_PROGRESS = "in_progress"
  COMPLETE = "complete"


# Firebase data model in "tasks" collection.
class Task(Model):
  """Task ORM class"""

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "tasks"

  id = IDField()
  title = TextField()
  description = TextField()
  step = TextField()
  status = TextField()
  created_at = Field()
  modified_at = Field()

  # Arbitrary data in JSON format.
  data = Field()

  @classmethod
  def find_by_id(cls, id):
    try:
      task = Task.collection.get(id)
    except ReferenceDocNotExist:
      return None

    return task
