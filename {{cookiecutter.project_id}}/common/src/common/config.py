"""
Config module to setup common environment
"""

import os

PROJECT_ID = os.environ.get("PROJECT_ID", "")

if PROJECT_ID != "":
  os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

NEO4J_URI = "bolt://neo4j-neo4j:7687"
