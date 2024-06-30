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
Pydantic Model for Task API's
"""
from typing import Optional
from pydantic import BaseModel
import time


class TaskSchema(BaseModel):
  """Task Pydantic Model"""

  # This is the reference API spec for Task data model.
  id: Optional[str]
  title: str
  description: str
  step: str
  status: str
  data: object
  created_at: Optional[str]
  modified_at: Optional[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "title": "Title",
            "description": "Description",
            "step": "step-1",
            "status": "new",
            "data": "test data",
        }
    }
