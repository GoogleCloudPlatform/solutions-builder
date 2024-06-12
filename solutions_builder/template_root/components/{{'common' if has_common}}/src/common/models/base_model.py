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
FireO BaseModel to be inherited by all other objects in ORM
"""
import datetime
from typing import List, Tuple
import fireo
from fireo.models import Model
from fireo.fields import DateTime, TextField
from fireo.fields.errors import (RequiredField,
                                 UnSupportedAttribute,
                                 FieldValidationFailed,
                                 ValidatorNotCallable)
from common.utils.errors import ResourceNotFoundException
import common.config


# pylint: disable = too-few-public-methods, arguments-renamed
class BaseModel(Model):
  """BaseModel to add common helper methods to all FireO objects

    An interface, intended to be subclassed.

    """
  created_time = DateTime()
  last_modified_time = DateTime()
  deleted_at_timestamp = DateTime(default=None)
  deleted_by = TextField(default="")
  archived_at_timestamp = DateTime(default=None)
  archived_by = TextField(default="")
  created_by = TextField(default="")
  last_modified_by = TextField(default="")
  DATABASE_PREFIX = common.config.DATABASE_PREFIX

  def save(self,
           input_datetime=None,
           transaction=None,
           batch=None,
           merge=None,
           no_return=False):
    """overrides default method to save items with timestamp
    Args:
      input_datetime (_type_, optional): _description_. Defaults to None.
      transaction (_type_, optional): _description_. Defaults to None.
      batch (_type_, optional): _description_. Defaults to None.
      merge (_type_, optional): _description_. Defaults to None.
      no_return (bool, optional): _description_. Defaults to False.
    Returns:
      _type_: _description_
    """
    if input_datetime:
      date_timestamp = input_datetime
    else:
      date_timestamp = datetime.datetime.utcnow()
    self.created_time = date_timestamp
    self.last_modified_time = date_timestamp
    return super().save(transaction, batch, merge, no_return)

  def update(self,
             input_datetime=None,
             key=None,
             transaction=None,
             batch=None):
    """overrides default method to update items with timestamp
    Args:
      input_datetime (_type_, optional): _description_. Defaults to None.
      key (_type_, optional): _description_. Defaults to None.
      transaction (_type_, optional): _description_. Defaults to None.
      batch (_type_, optional): _description_. Defaults to None.
    Returns:
      _type_: _description_
    """
    if input_datetime:
      date_timestamp = input_datetime
    else:
      date_timestamp = datetime.datetime.utcnow()
    self.last_modified_time = date_timestamp
    return super().update(key, transaction, batch)

  def get_fields(self, reformat_datetime=False):
    """overrides default method to fix data type for datetime fields"""
    fields = super()._get_fields()
    if "id" in self.to_dict():
      fields["id"] = self.id
    if reformat_datetime:
      fields["created_time"] = str(fields["created_time"])
      fields["last_modified_time"] = str(fields["last_modified_time"])
    return fields

  class Meta:
    # TODO: uncomment when bug is fixed
    # ignore_none_field seems not to inherit
    # will need to set on all end Models
    # https://github.com/octabytes/FireO/issues/106
    # ignore_none_field = False
    # commenting until it does something
    abstract = True

  @classmethod
  def find_by_id(cls, doc_id):
    """Looks up in the Database and returns an object of this type by id
       (not key)
        An interface, intended to be subclassed.
        Args:
            doc_id (string): the document id without collection_name
            (i.e. not the key)
        Returns:
            [any]: an instance of object returned by the database, type is
            the subclassed Model
        """
    obj = cls.collection.filter("id", "in",
                                [doc_id]).filter("deleted_at_timestamp",
                                                    "==", None).get()
    if obj is None:
      raise ResourceNotFoundException(
          f"{cls.collection_name} with id {doc_id} is not found")
    return obj

  @classmethod
  def delete_by_id(cls, doc_id):
    """Deletes from the Database the object of this type by id (not key)

        Args:
            doc_id (string): the document id without collection_name
            (i.e. not the key)

        Returns:
            None
        """
    key = fireo.utils.utils.generateKeyFromId(cls, doc_id)
    return cls.collection.delete(key)

  @classmethod
  def soft_delete_by_id(cls, object_id, by_user=None):
    """Soft delete an object by id
      Args:
          object_id (str): unique id
          by_user
      Raises:
          ResourceNotFoundException: If the object does not exist
      """
    obj = cls.collection.filter("id", "in",
                                [object_id]).filter("deleted_at_timestamp",
                                                    "==", None).get()
    if obj is None:
      raise ResourceNotFoundException(
          f"{cls.collection_name} with id {object_id} is not found")
    else:
      obj.deleted_at_timestamp = datetime.datetime.utcnow()
      obj.deleted_by = by_user
      obj.update()

  @classmethod
  def archive_by_id(cls, object_id, by_user=None):
    """_summary_
    Args:
      object_id (str): unique id
      by_user
    """
    obj = cls.collection.filter("id", "in",
                                [object_id]).filter("deleted_at_timestamp",
                                                    "==", None).get()
    if obj is None:
      raise ResourceNotFoundException(
          f"{cls.collection_name} with id {object_id} is not found")
    else:
      obj.archived_at_timestamp = datetime.datetime.utcnow()
      obj.archived_by = by_user
      obj.update()

  @classmethod
  def fetch_all(cls, skip=0, limit=1000, order_by="-created_time"):
    """ fetch all documents

    Args:
        skip (int, optional): _description_. Defaults to 0.
        limit (int, optional): _description_. Defaults to 1000.
        order_by (str, optional): _description_. Defaults to "-created_time".

    Returns:
        list: list of objects
    """
    objects = cls.collection.filter(
        "deleted_at_timestamp", "==",
        None).order(order_by).offset(skip).fetch(limit)
    return list(objects)

  @classmethod
  def fetch_all_documents(cls, limit=1000):
    """Fetches all documents of the collection in batches

    Args:
      limit (int): the number of documents to fetch in a batch

    Returns:
      list (document objects): list of firestore document objects
    """
    all_docs = []
    docs = cls.collection.fetch(limit)
    while True:
      batch_docs = list(docs)
      if not batch_docs:
        break
      all_docs.extend(batch_docs)
      docs.next_fetch(limit)
    return all_docs

  @classmethod
  def delete_by_uuid(cls, uuid):
    doc = cls.collection.filter("uuid", "==",
                                uuid).filter("is_deleted", "==", False).get()
    if doc is not None:
      doc.is_deleted = True
      doc.update()
    else:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")

  @classmethod
  def archive_by_uuid(cls, uuid, archive=True):
    doc = cls.collection.filter("uuid", "==",
                                uuid).filter("is_deleted", "==", False).get()
    if doc is not None:
      doc.is_archived = archive
      doc.update()
    else:
      raise (ResourceNotFoundException(
        f"{cls.__name__} with uuid {uuid} not found"))

  def validate(self) -> Tuple[bool, List[str]]:
    """
    Validate a model in this class.

    Returns:
      True,[] or False, list of error messages
    """
    errors = []
    valid = True
    for field_name, field in self._meta.field_list.items():
      val = getattr(self, field_name)
      field_attribute = field.field_attribute
      try:
        field_attribute.parse(val, ignore_required=False, ignore_default=False,
                              run_only=None)
      except RequiredField as e:
        valid = False
        errors.append(f"field '{field_name}': {str(e)}")
      except UnSupportedAttribute as e:
        valid = False
        errors.append(f"field '{field_name}': {str(e)}")
      except FieldValidationFailed as e:
        valid = False
        errors.append(f"field '{field_name}': {str(e)}")
      except ValidatorNotCallable as e:
        valid = False
        errors.append(f"field '{field_name}': {str(e)}")
    return valid, errors
