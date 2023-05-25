"""
Data model for Todo list.
"""

import os

from firedantic import Model
from firedantic.exceptions import ModelNotFoundError
from datetime import datetime

# GCP project_id from system's environment variable.
PROJECT_ID = os.environ.get("PROJECT_ID", "")

# Database prefix for integration and e2e test purpose.
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")


# Firebase data model in "todos" collection.
class Todo(Model):
  """Todo ORM class"""
  __collection__ = "todos"

  id: str = "1234"
  title: str = "Title"
  description: str = "Description"
  is_done: bool = False
  created_at: datetime
  modified_at: datetime = None

  @classmethod
  def find_by_id(cls, id):
    try:
      todo = Todo.get_by_doc_id(id)
    except ModelNotFoundError:
      return None

    return todo
