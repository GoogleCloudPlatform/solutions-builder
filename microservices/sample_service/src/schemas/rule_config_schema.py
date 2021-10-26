"""
  Pydantic schemas for Rules Config API's
"""
from pydantic import BaseModel


class GetRuleConfigIn(BaseModel):
  rule_id: str


class GetRuleConfigOut(BaseModel):
  rule_name: str
  base_weight: int
  incremental_weight: int
  threshold: int
  is_enabled: bool


class PostRuleConfigIn(GetRuleConfigOut):
  rule_id: str

  class Config:
    schema_extra = {
        "example": {
            "rule_id": "dup_full_mail_addr_count",
            "rule_name": "duplicate mail full address",
            "base_weight": 100,
            "incremental_weight": 10,
            "threshold": 5,
            "is_enabled": True
        }
    }


class PostRuleConfigOut(BaseModel):
  rule_id: str
