"""
Unit Tests for Claim ORM object
"""

from common.models import Claim


def test_new_claim():
  # a placeholder unit test so github actions runs until we add more
  claim_id = "test_id123"
  claim = Claim(claim_id=claim_id)

  assert claim.claim_id == claim_id
