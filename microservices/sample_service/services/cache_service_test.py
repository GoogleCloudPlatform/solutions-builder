"""
    utility methods to execute unit tests for module cache_service.py
"""
import pytest
import mock
import json
import time
from services.cache_service import set_key, get_key

dummy_data = {
    "name": "Alice",
    "is_user": True,
    "session_details": {
        "is_completed": False,
        "completed_percentage": 42,
        "created_at": time.time(),
        "context_ref": "level0/abc/level1/pqr/level2/xyz"
    },
    "user_id": "bh67Y-unByQAs4-oki8907hk",
    "completed_modules": ["module1", "module2"],
    "covered_lus": [],
    "activity_id": None,
    "answer": ""
}


@pytest.mark.parametrize("key, value", list(dummy_data.items()))
@mock.patch("services.cache_service.r.set")
def test_set_key(mock_set, key, value):
  # arrange
  mock_set.return_value = True

  # action
  cache_status = set_key(key, value)

  # assert
  assert cache_status is True


@mock.patch("services.cache_service.r.set")
def test_set_key_with_expiry(mock_set):

  mock_set.return_value = True
  cache_status = set_key("dummy_data", dummy_data, 1800)
  # assert
  assert cache_status


@pytest.mark.parametrize("key", list(dummy_data.keys()))
@mock.patch("services.cache_service.r.get")
def test_get_key_with(mock_get, key):
  # arrange
  mock_get.return_value = json.dumps(dummy_data[key]).encode("utf-8")

  # action
  cached_value = get_key(key)

  # assert
  assert cached_value == dummy_data[key]


@mock.patch("services.cache_service.r.get")
def test_get_key_with_expiry(mock_get):
  # arrange
  mock_get.return_value = json.dumps(dummy_data).encode("utf-8")

  # action
  cached_value = get_key("dummy_data")

  # assert
  assert cached_value == dummy_data
