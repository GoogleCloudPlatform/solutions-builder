"""Utility methods for database related operations."""
import google.auth
from google.cloud import firestore


def get_firestore_instance():
  """
            This method creates a firestore instance and returns it
            Args:
                None
            Returns:
                firestore client generator object: Reference
        """
  cred, project = google.auth.default()
  db = firestore.Client(project=project, credentials=cred)
  return db


def user_exist(collection_name, user_email):
  """
            This method checks for user existence in database
            Args:
                collection_name: String
                user_email: String
            Returns:
                True or False
        """
  db = get_firestore_instance()
  doc_ref = db.collection(u"{}".format(collection_name))
  query = doc_ref.where(u"email", u"==", u"{}".format(user_email))
  docs = query.get()
  return len(list(docs)) > 0


def insert_document(collection_name, data, doc_id):
  """
            This method insert document in firestore collection
            Args:
                collection_name: String
                data: Dict(Object)
                doc_id: String
            Returns:
                doc_status: Dict(Object)
        """
  db = get_firestore_instance()
  doc_status = db.collection(u"{}".format(collection_name)) \
      .document(u"{}".format(u"{}".format(doc_id))).set(data)
  return doc_status
