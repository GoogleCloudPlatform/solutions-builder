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
User Data Model
"""
import regex
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException
from fireo.fields import (TextField, NumberField, MapField, ListField, BooleanField)

USER_TYPES = ["learner", "faculty", "assessor", "admin", "coach", "instructor"]


def validate_name(name):
  """Validator method to validate name"""
  if regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", name):
    return True
  else:
    return False, "Invalid name format"


def check_user_type(field_val):
  """validator method for user type field"""
  if field_val.lower() in USER_TYPES:
    return True
  return (False, "User Type must be one of " +
          ",".join("'" + i + "'" for i in USER_TYPES))


def check_status(field_val):
  """validator method for status field"""
  status = ["active", "inactive"]
  if field_val.lower() in ["active", "inactive"]:
    return True
  return (False,
          "Status must be one of " + ",".join("'" + i + "'" for i in status))


def check_association_type(field_val):
  """validator method for association type field"""
  association_types = ["learner", "discipline"]
  if field_val.lower() in association_types:
    return True
  return (False, "Association Type must be one of " +
          ",".join("'" + i + "'" for i in association_types))


class User(BaseModel):
  """User base Class"""
  user_id = TextField(required=True)
  first_name = TextField(required=True, validator=validate_name)
  last_name = TextField(required=True, validator=validate_name)
  email = TextField(required=True, to_lowercase=True)
  user_type = TextField(required=True, validator=check_user_type)
  user_type_ref = TextField()
  user_groups = ListField()
  status = TextField(validator=check_status)
  is_registered = BooleanField()
  failed_login_attempts_count = NumberField()
  access_api_docs = BooleanField(default=False)
  gaia_id = TextField()
  photo_url = TextField()
  inspace_user = MapField(default={})
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "users"
    ignore_none_field = False

  @classmethod
  def find_by_user_id(cls, user_id, is_deleted=False):
    """Find the user using user_id
    Args:
        user_id (string): user_id of user
        is_deleted
    Returns:
        user Object
    """
    user = cls.collection.filter(
      "user_id", "==", user_id).filter("is_deleted", "==", is_deleted).get()
    if user is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with user_id {user_id} not found")
    return user

  @classmethod
  def find_by_uuid(cls, user_id, is_deleted=False):
    """Find the user using user_id
    Args:
        user_id (string): user_id of user
        is_deleted
    Returns:
        user Object
    """
    user = cls.collection.filter(
      "user_id", "==", user_id).filter("is_deleted", "==", is_deleted).get()
    if user is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with user_id {user_id} not found")
    return user

  @classmethod
  def find_by_email(cls, email):
    """Find the user using email
    Args:
        email (string): user's email address
    Returns:
        User: User Object
    """
    if email:
      email = email.lower()
    return cls.collection.filter("email", "==", email).get()

  @classmethod
  def find_by_status(cls, status):
    """Find the user using status
    Args:
        status (string): user's status
    Returns:
        List of User objects
    """
    return cls.collection.filter(
      "status", "==", status).filter("is_deleted", "==", False).fetch()

  @classmethod
  def find_by_gaia_id(cls, gaia_id, is_deleted=False):
    """Find the user using gaia id
    Args:
        gaia_id (string): user's gaia_id
        is_deleted
    Returns:
        User: User Object
    """
    user = cls.collection.filter(
      "gaia_id", "==", gaia_id).filter("is_deleted", "==", is_deleted).get()
    if user is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with gaia_id {gaia_id} not found")
    return user

  @classmethod
  def find_by_user_type_ref(cls, user_type_ref, is_deleted=False):
    """Find the user using user_type_ref/learner_id
    Args:
      user_type_ref (string): User's user_type_ref
      is_deleted
    Returns:
      User: User Object
    """
    user = cls.collection.filter(
      "user_type_ref", "==", user_type_ref).filter(
      "is_deleted", "==", is_deleted).get()
    if user is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with user_type_ref {user_type_ref} not found")
    return user

  @classmethod
  def delete_by_uuid(cls, uuid):
    """Delete the user using user id
    Args:
        uuid (string): user's user_id
    Returns:
        None
    """
    user = cls.collection.filter(
      "user_id", "==", uuid).filter("is_deleted", "==", False).get()
    if user is not None:
      user.is_deleted = True
      user.update()
    else:
      raise ResourceNotFoundException(
          f"{cls.__name__} with user_id {uuid} not found")


class UserGroup(BaseModel):
  """UserGroup Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  alias = TextField(default="security groups")
  users = ListField(default=[])
  roles = ListField(default=[])
  permissions = ListField(default=[])
  applications = ListField(default=[])
  is_immutable = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "user_groups"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the group using uuid
    Args:
        uuid (string): uuid of group
    Returns:
        group Object
    """
    group = cls.collection.filter("uuid", "==", uuid).get()
    if group is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return group

  @classmethod
  def find_by_name(cls, name):
    """Find the UserGroup using name
    Args:
        name (string): node item name
    Returns:
        UserGroup: UserGroup Object
    """
    return cls.collection.filter("name", "==", name).get()


class Permission(BaseModel):
  """Permission Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  application_id = TextField(required=True)
  module_id = TextField(required=True)
  action_id = TextField(required=True)
  user_groups = ListField(default=[])

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "permissions"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the permission using uuid
    Args:
        uuid (string): uuid of permission
    Returns:
        permission Object
    """
    permission = cls.collection.filter("uuid", "==", uuid).get()
    if permission is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return permission

  @classmethod
  def find_by_name(cls, name):
    """Find the Permission using name
    Args:
        name (string): node item name
    Returns:
        Permission: Permission Object
    """
    return cls.collection.filter("name", "==", name).get()


class Application(BaseModel):
  """Application Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  modules = ListField(default=[])

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "applications"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the application using uuid
    Args:
        uuid (string): uuid of application
    Returns:
        Application Object
    """
    application = cls.collection.filter("uuid", "==", uuid).get()
    if application is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return application

  @classmethod
  def find_by_name(cls, name):
    """Find the application using name
    Args:
        name (string): node item name
    Returns:
        Application: Application Object
    """
    return cls.collection.filter("name", "==", name).get()


def check_action_type(field_val):
  """validator method for action_type field"""
  action_types = ["main", "other"]
  if field_val.lower() in action_types:
    return True
  return (False, "action_type must be one of " +
          ",".join("'" + i + "'" for i in action_types))


class Action(BaseModel):
  """Action Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  action_type = TextField(validator=check_action_type)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "actions"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the scope using uuid
    Args:
        uuid (string): uuid of scope
    Returns:
        scope Object
    """
    scope = cls.collection.filter("uuid", "==", uuid).get()
    if scope is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return scope

  @classmethod
  def find_by_name(cls, name):
    """Find the Action using name
    Args:
        name (string): node item name
    Returns:
        Action: Action Object
    """
    return cls.collection.filter("name", "==", name).get()


class Module(BaseModel):
  """Module Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  actions = ListField(default=[])

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "modules"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find the module using uuid
    Args:
        uuid (string): uuid of module
    Returns:
        module Object
    """
    module = cls.collection.filter("uuid", "==", uuid).get()
    if module is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return module

  @classmethod
  def find_by_name(cls, name):
    """Find the module using name
    Args:
        name (string): node item name
    Returns:
        Module: Module Object
    """
    return cls.collection.filter("name", "==", name).get()
