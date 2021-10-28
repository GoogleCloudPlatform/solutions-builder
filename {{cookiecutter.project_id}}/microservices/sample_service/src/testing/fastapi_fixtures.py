"""
  Pytest Fixture for getting testclient from fastapi
"""
import pytest
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client_with_emulator(clean_firestore, scope="module"):
  test_client = TestClient(app)
  yield test_client
