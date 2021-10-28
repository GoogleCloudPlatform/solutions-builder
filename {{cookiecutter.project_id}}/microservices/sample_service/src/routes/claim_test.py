"""
  Tests for Claim endpoints
"""
import os
import json
import datetime
from .config_test import API_URL, TESTDATA_FILENAME, TEST_CLAIM

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from testing.fastapi_fixtures import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.models import Claim
import mock

# assigning url
api_url = API_URL

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}


def test_get_claim(client_with_emulator):
  claim_dict = TEST_CLAIM
  claim = Claim.from_dict(claim_dict)
  claim.save()

  url = api_url + f"/claim/{claim.claim_id}"
  data = TEST_CLAIM
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 200, "Status 200"
  assert json_response == data, "Response received"


def test_get_claims_negative(client_with_emulator):
  claim_id = "U2DDBkl3Ayg0PWudzhI"
  url = api_url + f"/claim/{claim_id}"
  data = {"detail": "Claim not found"}
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_post_claim_new(client_with_emulator):
  input_claim = TEST_CLAIM
  url = api_url + "/claim"
  with mock.patch("routes.claim.stream_claim_to_bigquery"):
    with mock.patch("routes.claim.create_claim_neo4j"):
      with mock.patch("routes.claim.Logger"):
        resp = client_with_emulator.post(url, json=input_claim)

  assert resp.status_code == 200, "Status 200"

  # now see if GET endpoint returns same data
  url = api_url + f"/claim/{input_claim['claim_id']}"
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert json_response == input_claim

  # now check and confirm it is properly in the databse
  loaded_claim = Claim.find_by_claim_id(input_claim["claim_id"])
  loaded_claim_dict = loaded_claim.to_dict()

  # popping id and key for equivalency test
  loaded_claim_dict.pop("id")
  loaded_claim_dict.pop("key")

  timestamp = datetime.datetime.utcnow()

  # remove the timestamps since they aren't returned in the API
  # response doesn't include
  acceptable_sec_diff = 15
  created_timestamp = datetime.datetime.strptime(
      loaded_claim_dict.pop("created_timestamp"), "%Y-%m-%d %H:%M:%S.%f")
  last_updated_timestamp = datetime.datetime.strptime(
      loaded_claim_dict.pop("last_updated_timestamp"), "%Y-%m-%d %H:%M:%S.%f")

  assert (timestamp - created_timestamp).total_seconds() < acceptable_sec_diff
  assert (timestamp -
          last_updated_timestamp).total_seconds() < acceptable_sec_diff

  # assert that rest of the fields are equivalent
  assert loaded_claim_dict == input_claim


def test_put_claim(client_with_emulator):
  # create new claim with POST to get timestamps
  input_claim = TEST_CLAIM
  url = api_url + "/claim"
  with mock.patch("routes.claim.stream_claim_to_bigquery"):
    with mock.patch("routes.claim.create_claim_neo4j"):
      with mock.patch("routes.claim.Logger"):
        resp = client_with_emulator.post(url, json=input_claim)

  # modify claim
  input_claim["first_name"] = "Emmy"

  url = api_url + "/claim"
  resp_data = SUCCESS_RESPONSE
  with mock.patch("routes.claim.stream_claim_to_bigquery"):
    with mock.patch("routes.claim.update_claim_neo4j"):
      with mock.patch("routes.claim.Logger"):
        resp = client_with_emulator.put(url, json=input_claim)

  json_response = json.loads(resp.text)
  assert resp.status_code == 200, "Status 200"
  assert json_response == resp_data, "Response received"

  # now make sure claim is updated and updated_timestamp is changed
  url = api_url + f"/claim/{input_claim['claim_id']}"
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)

  assert json_response == input_claim

  # assert timestamp has been updated
  # loading from DB since not surfaced in API
  loaded_claim = Claim.find_by_claim_id(input_claim["claim_id"])

  created_timestamp = datetime.datetime.strptime(loaded_claim.created_timestamp,
                                                 "%Y-%m-%d %H:%M:%S.%f")
  last_updated_timestamp = datetime.datetime.strptime(
      loaded_claim.last_updated_timestamp, "%Y-%m-%d %H:%M:%S.%f")

  assert created_timestamp < last_updated_timestamp


def test_put_claim_negative(client_with_emulator):
  claim_dict = TEST_CLAIM
  claim = Claim.from_dict(claim_dict)
  claim.save()

  input_claim = TEST_CLAIM
  input_claim["claim_id"] = "U2DDBkl3Ayg0PWudzhI"

  url = api_url + "/claim"
  with mock.patch("routes.claim.stream_claim_to_bigquery"):
    with mock.patch("routes.claim.update_claim_neo4j"):
      with mock.patch("routes.claim.Logger"):
        resp = client_with_emulator.put(url, json=input_claim)

  assert resp.status_code == 404, "Status 404"


def test_delete_claim(client_with_emulator):
  claim_dict = TEST_CLAIM
  claim = Claim.from_dict(claim_dict)
  claim.save()

  # confirm in backend with API
  url = api_url + f"/claim/{claim.claim_id}"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 200, "Status 200"

  # now delete claim with API
  url = api_url + f"/claim/{claim.claim_id}"
  with mock.patch("routes.claim.delete_claim_in_bigquery"):
    with mock.patch("routes.claim.delete_claim_neo4j"):
      with mock.patch("routes.claim.Logger"):
        resp = client_with_emulator.delete(url)

  assert resp.status_code == 200, "Status 200"

  # now confirm claim gone with API
  url = api_url + f"/claim/{claim.claim_id}"
  resp = client_with_emulator.get(url)
  assert resp.status_code == 404, "Status 404"


def test_delete_claim_negative(client_with_emulator):
  claim_dict = TEST_CLAIM
  claim = Claim.from_dict(claim_dict)
  claim.save()

  url = api_url + "/claim/U2DDBkl3Ayg0PWudzhIi"
  with mock.patch("routes.claim.delete_claim_in_bigquery"):
    with mock.patch("routes.claim.delete_claim_neo4j"):
      with mock.patch("routes.claim.Logger"):
        resp = client_with_emulator.delete(url)

  data = {"detail": "Claim not found"}
  resp = client_with_emulator.delete(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_bulk_create_claim(client_with_emulator):
  url = api_url + "/claim/upload_bulk_claim"
  with open(TESTDATA_FILENAME, encoding="UTF-8") as claim_csv_file:
    with mock.patch("routes.claim.stream_claim_to_bigquery"):
      with mock.patch("routes.claim.create_claim_neo4j"):
        with mock.patch("routes.claim.Logger"):
          resp = client_with_emulator.post(
              url, files={"claim_csv_file": claim_csv_file})
  assert resp.status_code == 200, "Status 200"
  # TODO: check db, etc. like other tests
