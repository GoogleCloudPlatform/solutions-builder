import os
import argparse
import json

parser = argparse.ArgumentParser(description="DeepLit Backend API")
parser.add_argument(
    "--prod", type=bool, default=False, help="Input the Runtime Environment")
args = parser.parse_args()

dirname = os.path.dirname(__file__)

IS_DEVELOPMENT = not args.prod

with open("./configs/{}.json".format(
    "dev" if IS_DEVELOPMENT is True else "prod")) as handle:
  env = json.loads(handle.read())

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 8888
GCP_PROJECT = os.environ.get("GCP_PROJECT", env["project_id"])
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write"
]

BASE_URL = env["base_url"]

BASE_URL_V2 = env["base_url_v2"]

SERVICE = env["service"]

COLLECTION = env["collection"]

COLLECTION_NAME = env["collection_name"]

REDIS_HOST = env["redis_host"]

COURSE_CONTEXT_COLLECTION = env["course_context_collection"]

ACTIVITY_ID = "teachme"

SERVICES = {
    "authentication": {
        "host": "authentication",
        "port": 8889
    },
    "sample_service": {
        "host": "sample_service",
        "port": 8888
    },
    "utils": {
        "host": "utils",
        "port": 8891
    }
}

LEVEL_MAPPING = {
    "Course": "level0",
    "Program": "level0",
    "Competency": "level1",
    "http://purl.imsglobal.org/vocab/lis/v2/course#CourseOffering": "level1",
    "Units": "level1",
    "SubCompetency": "level2",
    "Modules": "level2"
}
