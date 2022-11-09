"""
  Pytest Fixture for getting testclient from fastapi
"""

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

import pytest
from .firestore_emulator import clean_firestore
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client_with_emulator(clean_firestore, scope="module"):
  test_client = TestClient(app)
  yield test_client
