"""
    utility methods to execute unit tests for module firestore_service.py
"""
import mock
import time
import uuid

from services.firestore_service import (get_doc_id, get_firestore_instance,
                                        apply_filters, insert_document,
                                        get_documents, get_document_by_id,
                                        check_document, update_document,
                                        get_leaf_document, check_session_exists)


class MockDocument:

  def __init__(self, data):
    self.id = str(uuid.uuid4())
    self.data = data


def get_doc_ref():
  yield MockDocument({"context_ref": "level0/abc/level1/pqr/level2/xyz"})


def test_get_doc_id():
  uid = get_doc_id()
  assert uid is not None
  assert isinstance(uid, str)
  assert len(uid) > 0


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

  assert db is not None
  assert len(mock_google_auth.mock_calls) == 1
  assert len(mock_google_auth.mock_calls[0].args) == 0
  assert len(mock_client.mock_calls) == 1
  assert len(mock_client.mock_calls[0].args) == 2
  assert mock_client.mock_calls[0].args[0] == project
  assert mock_client.mock_calls[0].args[1] == cred


def test_apply_filters():
  # arrange
  doc_ref = mock.Mock()
  filters = {
      "activity_id": "teachme",
      "is_active": True,
      "user_id": "zLpxCfnhrCVrcSDRAOLLougE7Q43"
  }
  # action
  doc_ref = apply_filters(doc_ref, filters)

  # assert
  assert doc_ref is not None


@mock.patch("services.firestore_service.get_firestore_instance")
def test_insert_document(mock_firestore):
  # arrange
  collection_name = "sessions"
  session_data = {
      "activity_id": "teachme",
      "completed_percentage": 0,
      "is_active": True,
      "start_time": time.time(),
      "context_ref": "level0/abc/level1/pqr/level2/xyz",
      "user_id": "zLpxCfnhrCVrcSDRAOLLougE7Q43"
  }
  mock_firestore.return_value = mock.Mock()

  # action
  session_id = insert_document(collection_name, session_data)
  call_stack = mock_firestore.mock_calls
  # assert
  print(call_stack)
  assert session_id is not None
  assert isinstance(session_id, str)
  assert len(session_id) > 0
  assert len(call_stack) == 4
  assert call_stack[1].args[0] == collection_name
  assert call_stack[2].args[0] == session_id
  assert call_stack[3].args[0] == session_data


@mock.patch("services.firestore_service.get_firestore_instance")
def test_check_document_exist(mock_firestore):
  # arrange
  collection_name = "sessions"
  field_path = "context_ref"
  value = "level0/abc/level1/pqr/level2/xyz"
  mock_firestore.return_value.collection\
      .return_value.where.return_value\
      .limit.return_value.get.return_value = get_doc_ref()

  # action
  doc_id = check_document(collection_name, field_path, value)

  # assert
  assert isinstance(doc_id, str)
  assert doc_id != "-1"
  assert len(doc_id) > 0


@mock.patch("services.firestore_service.get_firestore_instance")
def test_check_document_not_exist(mock_firestore):
  # arrange
  collection_name = "sessions"
  field_path = "context_ref"
  value = "level0/abc/level1/pqr/level2/xyz"
  mock_firestore.return_value.collection\
      .return_value.where.return_value\
      .limit.return_value.get.return_value = ()

  # action
  doc_id = check_document(collection_name, field_path, value)

  # assert
  mock_firestore.assert_called()
  assert doc_id == "-1"


@mock.patch("services.firestore_service.get_firestore_instance")
def test_get_documents(mock_firestore):
  # arrange
  collection_name = "sessions"
  mock_docs = [mock.Mock(id="1"), mock.Mock(id="2"), mock.Mock(id="3")]
  mock_firestore.return_value.collection\
      .return_value.get.return_value = mock_docs

  # action
  docs = get_documents(collection_name)

  # assert
  mock_firestore.asset_called()
  assert len(list(docs)) == 3


@mock.patch("services.firestore_service.get_firestore_instance")
def test_get_document_by_id(mock_firestore):
  # arrange
  collection_name = "sessions"
  session_id = str(uuid.uuid4())
  mock_firestore.return_value.collection\
      .return_value.document.return_value\
      .get.return_value = mock.Mock(id=session_id)

  # action
  doc = get_document_by_id(collection_name, session_id)

  # assert
  assert doc.id == session_id


@mock.patch("services.firestore_service.get_firestore_instance")
def test_update_document(mock_firestore):
  # arrange
  collection_name = "sessions"
  session_id = str(uuid.uuid4())
  data = {"is_active": False}
  mock_firestore.return_value.collection\
      .return_value.document.return_value = mock.Mock(id=session_id)

  # action
  doc_id = update_document(collection_name, session_id, data)

  # assert
  assert doc_id == session_id


@mock.patch("services.firestore_service.apply_filters")
@mock.patch("services.firestore_service.get_firestore_instance")
def test_get_leaf_document(mock_firestore, mock_filters):
  # arrange
  collection_name = "leavel2"
  filters = {
      "label": "SC-1",
      "title": "Sub-Competency 1",
      "type": "SubCompetency"
  }
  mock_firestore.collection_group.return_value = mock.Mock
  mock_filters.return_value.limit\
      .return_value.get.return_value = [mock.Mock(id="1", data=filters)]

  # action
  docs = get_leaf_document(collection_name, filters)

  # assert
  assert len(docs) == 1
  assert docs[0].id == "1"
  assert docs[0].data == filters


@mock.patch("services.firestore_service.apply_filters")
@mock.patch("services.firestore_service.get_firestore_instance")
def test_check_session_exists(mock_firestore, mock_filters):
  # arrange
  collection_name = "sessions"
  filters = {"is_active": True, "user_id": str(uuid.uuid4())}
  mock_firestore.collection.return_value = mock.Mock
  mock_filters.return_value.limit\
      .return_value.get.return_value = [mock.Mock(id="1", data=filters)]

  # action
  docs = check_session_exists(collection_name, filters)

  # assert
  assert len(docs) == 1
  assert docs[0].id == "1"
  assert docs[0].data["is_active"]
  assert docs[0].data["user_id"] == filters["user_id"]
