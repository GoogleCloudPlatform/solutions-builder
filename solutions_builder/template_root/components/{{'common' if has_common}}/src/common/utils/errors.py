# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Classes for handling errors
"""


class ResourceNotFoundException(Exception):
  """Error class to be raised when resource is not found"""

  def __init__(self, message="Resource not found"):
    self.message = message
    super().__init__(self.message)


class NoItemGeneratedError(Exception):
  """Class for custom Exceptions"""

  def __init__(self, message="No items were generated."):
    self.message = message
    super().__init__(self.message)


class InvalidFileType(Exception):
  """Error class to be raised when file with wrong/invalid ext is sent"""

  def __init__(self, message="Invalid file type"):
    self.message = message
    super().__init__(self.message)


class ValidationError(Exception):
  """Error class to be raised when there is a validation failed"""

  def __init__(self, message="Validation Failed", data=None):
    self.message = message
    self.data = data
    super().__init__(self.message)


class PreconditionFailedError(Exception):
  """Error class to be raised when there is a validation failed"""

  def __init__(self, message="Precondition Failed", data=None):
    self.message = message
    self.data = data
    super().__init__(self.message)


class ConflictError(Exception):
  """Error class to be raised when there is a conflict"""

  def __init__(self, message="Conflict"):
    self.message = message
    super().__init__(self.message)


class InvalidTokenError(Exception):
  """Error class to be raised when invalid auth token found"""

  def __init__(self, message="Invalid token"):
    self.message = message
    super().__init__(self.message)


class TokenNotFoundError(Exception):
  """Error class to be raised when auth token is not found"""

  def __init__(self, message="Token not found"):
    self.message = message
    super().__init__(self.message)


class InvalidCredentialsError(Exception):
  """Error class to be raised when invalid/incorrect credentials are passed"""

  def __init__(self, message="Invalid credentials"):
    self.message = message
    super().__init__(self.message)


class InvalidRequestPayloadError(Exception):
  """Error class to be raised when invalid payload is passed"""

  def __init__(self, message="Invalid request payload"):
    self.message = message
    super().__init__(self.message)


class UnauthorizedUserError(Exception):
  """Error class to be raised when unknown user tries to sign_up/sign_in"""

  def __init__(self, message="Unauthorized"):
    self.message = message
    super().__init__(self.message)


class PayloadTooLargeError(Exception):
  """Error class to be raised when payload is larger than the server is
  willing to process"""

  def __init__(self, message="Payload too large"):
    self.message = message
    super().__init__(self.message)

class InternalServerError(Exception):
  """Error class to be raised when internal server failure occurs"""

  def __init__(self, message="Internal Server Error"):
    self.message = message
    super().__init__(self.message)


class UserManagementServiceError(Exception):
  """Error class to be raised when there is error in user management service"""

  def __init__(self, message="Create User failed"):
    self.message = message
    super().__init__(self.message)


class CronJobException(Exception):
  """Error class to be raised when issue in executin gCronjob"""

  def __init__(self, message="Cronjob Error"):
    self.message = message
    super().__init__(self.message)


class BatchJobError(Exception):
  """Error class to be raised when an error occurs creating a batch job"""

  def __init__(self, message="Batch job creation error"):
    self.message = message
    super().__init__(self.message)
