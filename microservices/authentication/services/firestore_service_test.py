"""
    utility methods to execute unit tests for module firestore_service.py
"""
import mock
from services.firestore_service import (get_firestore_instance, insert_document,
                                        user_exist)

user_id = "fiurc756IqcdRSs19upxiVLt1Gr2"
test_user = {"email": "test.user@gmail.com", "name": "Test User"}


@mock.patch("services.firestore_service.firestore.Client")
@mock.patch("services.firestore_service.google.auth.default")
def test_get_firestore_instance(mock_google_auth, mock_client):
  # arrange
  cred = "default-credentials"
  project = "test-project"
  mock_google_auth.return_value = (cred, project)
  mock_client.return_value = mock.Mock()

  # action
  db = get_firestore_instance()

  # assert
  assert db is not None
  assert len(mock_google_auth.mock_calls) == 1
  assert len(mock_google_auth.mock_calls[0].args) == 0
  assert len(mock_client.mock_calls) == 1
  assert len(mock_client.mock_calls[0].kwargs) == 2
  assert mock_client.mock_calls[0].kwargs["project"] == project
  assert mock_client.mock_calls[0].kwargs["credentials"] == cred


@mock.patch("services.firestore_service.get_firestore_instance")
def test_insert_document(mock_firestore):
  # arrange
  collection_name = "users"
  mock_firestore.return_value.\
      collection.return_value\
      .document.return_value\
      .set.return_value = mock.Mock(id=user_id, data=test_user)

  # action
  doc_status = insert_document(collection_name, test_user, user_id)

  assert doc_status is not None
  assert doc_status.id == user_id
  assert doc_status.data == test_user


@mock.patch("services.firestore_service.get_firestore_instance")
def test_user_exist(mock_firestore):
  # arrange
  collection_name = "users"
  user_email = "test.user@gmail.com"

  mock_firestore.return_value\
      .collection.return_value\
      .where.return_value\
      .get.return_value = [
          mock.Mock(email="test.user@gmail.com", name="Test User")
      ]

  # action
  user_found = user_exist(collection_name, user_email)

  # assert
  assert user_found is True


@mock.patch("services.firestore_service.get_firestore_instance")
def test_user_not_exist(mock_firestore):
  # arrange
  collection_name = "users"
  user_email = "test.user@gmail.com"

  mock_firestore.return_value\
      .collection.return_value\
      .where.return_value\
      .get.return_value = []

  # action
  user_found = user_exist(collection_name, user_email)

  # assert
  assert user_found is False
