# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility methods for token validation."""
from firebase_admin.auth import verify_id_token
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from google.oauth2 import id_token
from google.auth.transport import requests

auth_scheme = HTTPBearer(auto_error=False)


def verify_oauth2_token(token: auth_scheme = Depends()):
  """
    Validates Token passed in headers, Returns user
    auth details along with user_type = new or old
    In case of Invalid token Throws error
    Args:
        Bearer Token: String
    Returns:
        Decoded Token and User type: Dict
  """
  print(f"Validating Token: {token}")

  if not token:
    raise HTTPException(status_code=401, detail="Invalid Token")

  try:
    print(f"Token: {token.credentials}")
    decoded_token = id_token.verify_oauth2_token(
        token.credentials, requests.Request())
    print(f"Decoded Token: {decoded_token}")
    return decoded_token

  except Exception as e:
    print(e)
    raise HTTPException(status_code=401, detail="Unauthorized")
