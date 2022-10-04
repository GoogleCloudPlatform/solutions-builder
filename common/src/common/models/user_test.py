"""
Unit Tests for user ORM object
"""

from common.models import User


def test_new_user():
  # a placeholder unit test so github actions runs until we add more
  user_id = "test_id123"
  user = User(user_id=user_id)

  assert user.user_id == user_id
