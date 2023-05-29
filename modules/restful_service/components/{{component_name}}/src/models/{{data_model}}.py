"""
Data model for {{data_model | capitalize}} list.
"""

import os

from firedantic import Model
from firedantic.exceptions import ModelNotFoundError
from datetime import datetime

# GCP project_id from system's environment variable.
PROJECT_ID = os.environ.get("PROJECT_ID", "")

# Database prefix for integration and e2e test purpose.
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")


# Firebase data model in "{{data_model_plural}}" collection.
class {{data_model | capitalize}}(Model):
  """{{data_model | capitalize}} ORM class"""
  __collection__ = "{{data_model_plural}}"

  id: str = "1234"
  title: str = "Title"
  description: str = "Description"
  is_done: bool = False
  created_at: datetime = None
  modified_at: datetime = None

  @classmethod
  def find_by_id(cls, id):
    try:
      {{data_model}} = {{data_model | capitalize}}.get_by_doc_id(id)
    except ModelNotFoundError:
      return None

    return {{data_model}}
