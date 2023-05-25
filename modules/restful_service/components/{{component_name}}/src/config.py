"""
  Sample Service config file
"""
import os

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID") or \
    os.environ.get("GOOGLE_CLOUD_PROJECT")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

COLLECTION = os.getenv("COLLECTION")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")
