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
