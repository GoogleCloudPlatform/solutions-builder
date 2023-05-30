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

"""
Pydantic Model for User API's
"""
from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
  """User Pydantic Model"""
  user_id: str
  first_name: str
  middle_name: Optional[str] = None
  last_name: str
  date_of_birth: str
  email_address: str


  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
        "user_id" : "fake-user-id",
        "first_name" : "Tony",
        "middle_name" : "I",
        "last_name" : "Stark",
        "date_of_birth" : "2001-07-16",
        "email_address" : "ironman@stark.com",
        "phone_num" : "5185550001",
      }
    }


class GcsBucketInfoModel(BaseModel):
  """Gcs Bucket blob Pydantic Model"""
  bucket_name: str
  file_name: str

  class Config():
    schema_extra = {
        "example": {
            "bucket_name": "client-users-data",
            "file_name": "all-users.csv"
        }
    }
