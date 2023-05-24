"""
DB Client fixture for re-use in testing
"""

import pytest
from google.cloud.bigquery import Client

client = Client()


@pytest.fixture(scope="module")
def client_fixture():
  yield client
