"""Utility methods for caching related operations."""
import json
import redis
from config import REDIS_HOST

r = redis.Redis(host=REDIS_HOST, port=6379, db=0)


def set_key(key, value, expiry_time=3600):
  """
        Stores value against key in cache with default expiry time of 1hr
        Args:
            key: String
            value: String or Dict or Number
            exp: Number(Expiry time in Secs, default 3600)
        Returns:
            True or False
    """
  value = json.dumps(value)
  return r.set(key, value, ex=expiry_time)


def get_key(key):
  """
        Checks for key in cache, if found then, Returns value against that key
        else Returns None
        Args:
            key: String
        Returns:
            value: String or Dict or Number or None
    """
  value = r.get(key)
  return_value = json.loads(value) if value is not None else None
  return return_value
