"""
  Tests for endpoints related to rules config
"""
import json
import os
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from testing.fastapi_fixtures import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.models import Rule

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

api_url = "http://localhost/sample_service/v1"


def test_get_rule_config_correct(client_with_emulator):
  rule = Rule()
  rule.name = "dup full mail addr count"
  rule.fields = ["mail_address_line1", "mail_address_line2"]
  rule.aggregation_type = "count"
  rule.count_columns = ["claim_id"]
  rule.is_enabled = True
  rule.output_columns = ["dup_full_mail_addr_count"]
  rule.sql_query = "SELECT mail_address_line1,mail_address_line2, \
    mail_address_city,mail_address_state,mail_address_zipcode, \
    COUNT(DISTINCT tax_payer_id) AS dup_full_mail_addr_count \
    FROM `solutions-template-dev.rules_engine.claims_test_data` \
    where trim(mail_address_line1) != " "\
    GROUP BY mail_address_line1,mail_address_line2,mail_address_city, \
    mail_address_state,mail_address_zipcode"

  rule.flag_condition = "greater than"
  rule.remark = "Same mail full address found"
  rule.base_weight = 35
  rule.incremental_weight = 10
  rule.threshold = 1
  rule.id = "dup_full_mail_addr_count"
  rule.save()
  url = api_url + f"/rule_config/{rule.id}"
  data = {
      "rule_name": "dup full mail addr count",
      "base_weight": 35,
      "incremental_weight": 10,
      "threshold": 1,
      "is_enabled": True
  }
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 200, "Status 200"
  assert json_response == data, "Response received"


def test_get_rule_config_incorrect(client_with_emulator):
  rule_id = "unknown"
  url = api_url + f"/rule_config/{rule_id}"
  data = {"detail": "Rule 'unknown' not found"}
  resp = client_with_emulator.get(url)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == data, "Response received"


def test_post_rule_config_correct(client_with_emulator):
  rule = Rule()
  rule.name = "dup full mail addr count"
  rule.fields = ["mail_address_line1", "mail_address_line2"]
  rule.aggregation_type = "count"
  rule.count_columns = ["claim_id"]
  rule.is_enabled = True
  rule.output_columns = ["dup_full_mail_addr_count"]
  rule.sql_query = "SELECT mail_address_line1,mail_address_line2, \
    mail_address_city,mail_address_state,mail_address_zipcode, \
    COUNT(DISTINCT tax_payer_id) AS dup_full_mail_addr_count \
    FROM `solutions-template-dev.rules_engine.claims_test_data` \
    where trim(mail_address_line1) != " "\
    GROUP BY mail_address_line1,mail_address_line2,mail_address_city, \
    mail_address_state,mail_address_zipcode"

  rule.flag_condition = "greater than"
  rule.remark = "Same mail full address found"
  rule.base_weight = 35
  rule.incremental_weight = 10
  rule.threshold = 1
  rule.id = "dup_full_mail_addr_count"
  rule.save()

  req_data = {
      "rule_id": "dup_full_mail_addr_count",
      "rule_name": "Changed Name",
      "base_weight": 40,
      "incremental_weight": 10,
      "threshold": 1,
      "is_enabled": False
  }
  url = api_url + "/rule_config"
  resp_data = {"rule_id": "dup_full_mail_addr_count"}
  resp = client_with_emulator.post(url, json=req_data)
  json_response = json.loads(resp.text)
  assert resp.status_code == 200, "Status 200"
  assert json_response == resp_data, "Response received"


def test_post_rule_config_incorrect(client_with_emulator):
  req_data = {
      "rule_id": "unknown_id",
      "rule_name": "duplicate mail full address",
      "base_weight": 36,
      "incremental_weight": 10,
      "threshold": 1,
      "is_enabled": True
  }
  url = api_url + "/rule_config"
  resp_data = {"detail": "unknown data"}
  resp = client_with_emulator.post(url, json=req_data)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404, "Status 404"
  assert json_response == resp_data, "Response received"
