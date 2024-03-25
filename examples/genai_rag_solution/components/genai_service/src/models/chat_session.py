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
Data model for Todo. See https://octabyte.io/FireO/ for details.
"""


# GCP project_id from system's environment variable.
import os
from fireo.models import Model
from fireo.fields import IDField, TextField, ListField, DateTime
from fireo.queries.errors import ReferenceDocNotExist


# Firebase data model in "chat_sessions" collection.
class ChatSession(Model):
  """Todo ORM class"""

  class Meta:
    ignore_none_field = False
    collection_name = "chat_sessions"

  id = IDField()
  email = TextField()
  history = ListField()
  created_at = DateTime()
  modified_at = DateTime()

  @classmethod
  def find_by_id(cls, id):
    try:
      print(f"Finding with id: {id}")
      chat_session = ChatSession.collection.get(f"chat_sessions/{id}")
    except ReferenceDocNotExist:
      return None

    return chat_session

  @classmethod
  def find_by_user(cls, email):
    try:
      chat_sessions = ChatSession.collection.filter(
          "email", "==", email).fetch()
    except ReferenceDocNotExist:
      return None

    return chat_sessions

