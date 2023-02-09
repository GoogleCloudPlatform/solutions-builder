"""
  Deletes datasets from firestore and bigquery when the github actions
  complete running tests
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore

PROJECT_ID = os.getenv("PROJECT_ID")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)

# Initializing Firebase client.
firebase_admin.initialize_app(credentials.ApplicationDefault(), {
    "projectId": PROJECT_ID,
})
db = firestore.client()

def delete_firestore_collection(collection_id):
  delete_collection(db.collection(collection_id), 10)


def delete_collection(coll_ref, batch_size):
  docs = coll_ref.limit(batch_size).stream()
  deleted = 0

  for doc in docs:
    doc.reference.delete()
    deleted = deleted + 1

  if deleted >= batch_size:
    return delete_collection(coll_ref, batch_size)


if __name__ == "__main__":
  if DATABASE_PREFIX is None:
    raise Exception("DATABASE_PREFIX is not defined. Database cleanup skipped.")

  print("Deleting Firebase collection")
  delete_firestore_collection(f"{DATABASE_PREFIX}document")
