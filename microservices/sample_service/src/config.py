"""
  Sample Service config file
"""
import os

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("GCP_PROJECT", os.environ.get("PROJECT_ID", ""))
if GCP_PROJECT != "":
  os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write"
]

COLLECTION = os.getenv("COLLECTION")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")
