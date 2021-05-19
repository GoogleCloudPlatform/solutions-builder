"""Utility methods for database related operations."""
from uuid import uuid4
import google.auth
from google.cloud import firestore
from utils.logging_handler import Logger


def get_doc_id():
  """
        This method returns a randomly generated unique id
        Args:
            None
        Returns:
            unique id: String
    """
  return str(uuid4())


def get_firestore_instance():
  """
        This method creates a firestore instance and returns it
        Args:
            None
        Returns:
            firestore client generator object: Reference
    """
  Logger.info("Creating Firestore instance")
  cred, project = google.auth.default()
  db = firestore.Client(project, cred)
  return db


def apply_filters(doc_ref, filters):
  """
        This method apply filters to the doc_ref passed in method parameter
        and returns doc_ref
        Args:
            doc_ref: Query object(Reference)
            filters: Dict
        Returns:
            doc_ref: Query object(Reference)
    """

  for filter_ in filters:
    doc_ref = doc_ref.where(u"{}".format(filter_), u"==", filters[filter_])
  return doc_ref


def insert_document(collection_name, data):
  """
        This method insert document in firestore collection and
        returns document id
        Args:
            collection_name: String
            data: Dict
        Returns:
            doc_id: String
    """
  db = get_firestore_instance()
  doc_id = get_doc_id()
  doc_insert_status = db.collection(u"{}".format(collection_name)).document(
      u"{}".format(doc_id)).set(data)
  Logger.info("New document insert status: {}".format(doc_insert_status))
  return doc_id


def check_document(collection_name, field_path, value):
  """
        This method checks if document with particular field exist in
        collection_name, Returns doc_id if exist else -1
        Args:
            collection_name: String
            field_path: String
            value: String or Boolean or Number
        Returns:
            id: String
    """
  db = get_firestore_instance()
  docs_ref = db.collection(u"{}".format(collection_name)) \
      .where(u"{}".format(field_path), u"==", u"{}".format(value)).limit(1)
  docs = docs_ref.get()
  doc_list = list(docs)
  if len(doc_list) > 0:
    return doc_list[0].id
  return "-1"


def get_documents(collection_name):
  """
        This method returns all the documents from that collection
        Args:
            collection_name: String
        Returns:
            docs: Generator Object(Reference)
    """
  db = get_firestore_instance()
  doc_ref = db.collection(u"{}".format(collection_name))
  docs = doc_ref.get()
  return docs


def get_document_by_id(collection_name, doc_id):
  """
        This method will return document with that particular doc_id
        Args:
            collection_name: String
            doc_id: String
        Returns:
            docs: DocumentSnapshot object(Reference)
    """
  Logger.info("Retrieving session based on Doc ID")
  db = get_firestore_instance()
  doc = db.collection(u"{}".format(collection_name)).document(
      u"{}".format(doc_id)).get()
  return doc


def update_document(collection_name, doc_id, data):
  """
        This method takes collection_name and doc_id as parameters
        and updates document with data
        Args:
            collection_name: String
            doc_id: string
            data: Dict
        Returns:
            id: String
    """
  db = get_firestore_instance()
  doc_ref = db.collection(u"{}".format(collection_name)).document(
      u"{}".format(doc_id))
  doc_ref.update(data)
  return doc_ref.id


def get_leaf_document(collection_name, filters=None):
  """
        This method fetches single document from subcollection
        which satisfies conditions passed in filters.
        Args:
            collection_name: String
            filters: Dict
        Returns:
            doc: Generator Object(Reference)
    """
  db = get_firestore_instance()
  doc_ref = db.collection_group(u"{}".format(collection_name))
  doc_ref = apply_filters(doc_ref, filters) if filters is not None else doc_ref
  query = doc_ref.limit(1)
  docs = query.get()
  return docs


def check_session_exists(collection_name, filters=None):
  """
        This method checks if there exist a session satisfying
        all the conditions passed in filters.
        Returns a single document in list if session exist else empty list
        Args:
            collection_name: String
            filters: Dict
        Returns:
            docs: List of DocumentSnapshot Object(Reference)
            or Empty List
    """
  db = get_firestore_instance()
  doc_ref = db.collection(u"{}".format(collection_name))
  doc_ref = apply_filters(doc_ref, filters) if filters is not None else doc_ref
  query = doc_ref.limit(1)
  docs = query.get()
  return list(docs)
