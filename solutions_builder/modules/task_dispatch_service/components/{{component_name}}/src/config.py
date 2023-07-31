"""
Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
"""
  Sample Service config file
"""
import os

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID") or \
    os.environ.get("GOOGLE_CLOUD_PROJECT")
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
SERVICE_NAME = os.getenv("SERVICE_NAME")
TASK_TOPIC = "{{task_pubsub_topic}}"
WORKFLOW_PATH = os.getenv("WORKFLOW_PATH")
