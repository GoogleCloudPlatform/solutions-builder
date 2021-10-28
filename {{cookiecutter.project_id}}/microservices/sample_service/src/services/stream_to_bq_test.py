"""
  Tests for claims insert,update and delete in Bigquery
"""
import copy
import json
import config
import datetime
from unittest.mock import Mock
from testing.test_config import TEST_INPUT_CLAIM, CLAIM_ID
from common.utils.stream_to_bq import stream_claim_to_bigquery, delete_claim_in_bigquery

client = Mock()


#Test create claim
def test_create_claim():
  claim = copy.deepcopy(TEST_INPUT_CLAIM)
  timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
  stream_claim_to_bigquery(client, claim, "CREATE", timestamp)
  claim_expected = copy.deepcopy(TEST_INPUT_CLAIM)
  del claim_expected["document_details"]
  claim_expected["operation"] = "CREATE"
  claim_expected["timestamp"] = timestamp
  claim_expected["created_timestamp"] = timestamp
  claim_expected["last_updated_timestamp"] = timestamp
  claim_expected["all_document_details"] = json.dumps(
      TEST_INPUT_CLAIM.get("document_details"))
  client.insert_rows_json.assert_called_with(
      f"{config.PROJECT_ID}.rules_engine.claims", [claim_expected])


#Test update claim
def test_update_claim():
  claim = copy.deepcopy(TEST_INPUT_CLAIM)
  timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
  stream_claim_to_bigquery(client, claim, "UPDATE", timestamp)
  claim_expected = copy.deepcopy(TEST_INPUT_CLAIM)
  del claim_expected["document_details"]
  claim_expected["operation"] = "UPDATE"
  claim_expected["timestamp"] = timestamp
  claim_expected["created_timestamp"] = timestamp
  claim_expected["last_updated_timestamp"] = timestamp
  claim_expected["all_document_details"] = json.dumps(
      TEST_INPUT_CLAIM.get("document_details"))
  client.insert_rows_json.assert_called_with(
      f"{config.PROJECT_ID}.rules_engine.claims", [claim_expected])


#Test delete claim
def test_delete_claim():
  timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
  delete_claim_in_bigquery(client, CLAIM_ID, timestamp)
  test_claim = {}
  test_claim["claim_id"] = CLAIM_ID
  test_claim["operation"] = "DELETE"
  test_claim["timestamp"] = timestamp
  test_claim["created_timestamp"] = timestamp
  test_claim["last_updated_timestamp"] = timestamp
  client.insert_rows_json.assert_called_with(
      f"{config.PROJECT_ID}.rules_engine.claims", [test_claim])
