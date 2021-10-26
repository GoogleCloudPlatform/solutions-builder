"""
  Pydantic schemas for Risk Profile API's
"""
from typing import List, Optional
from pydantic import BaseModel

extra_response_codes = {204: {"description": "Still calculating risk profile"}}


class RuleList(BaseModel):
  rule_id: Optional[str] = None
  rule_description: Optional[str] = None
  total_weight: Optional[int] = 0
  similar_claim_ids: List[str]
  comments: Optional[str] = None


class SimilarityProfile(BaseModel):
  claim_id: str
  relationship_list: List[str]


class RiskProfileClaim(BaseModel):
  """ Pydantic Model for response of Risk Profile API """
  claim_id: str
  num_flags: int
  flag_score: int
  flag_list: Optional[List[RuleList]] = []
  rules_engine_status: str
  similarity_claim_list: Optional[List[SimilarityProfile]] = []
  similarity_engine_status: str

  class Config:
    schema_extra = {
        "example": {
            "claim_id": "7888fccf-89f1-4a8a-9dec-81ed57eeb6bb",
            "num_flags": 1,
            "flag_score": 100,
            "flag_list": [{
                "rule_id":
                    "dup_email_addr_count",
                "rule_description":
                    "same email address found: Same email found in application",
                "total_weight":
                    100,
                "similar_claim_ids": [
                    "d829dad5-b451-490e-8bd9-c91c6c32fdfc",
                    "7888fccf-89f1-4a8a-9dec-81ed57eeb6bb"
                ],
                "comments":
                    "Same email address found in application"
            }],
            "rules_engine_status": "Success",
            "similarity_claim_list": [{
                "claim_id": "6551e4f6-a87c-46d3-b8c3-d9ae53bbb8b9",
                "relationship_list": ["SAME_MA", "SAME_RA"]
            }],
            "similarity_engine_status": "Success"
        }
    }
