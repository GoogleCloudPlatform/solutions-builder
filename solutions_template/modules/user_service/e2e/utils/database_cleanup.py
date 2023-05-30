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
