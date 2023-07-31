/**
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

# TODO: Add Terraform variable with Jinja variables below.
# Note for modules: Jinja variables are defined in copier.yaml.


project_id                 = "{{project_id}}"
region                     = "{{gcp_region}}"
task_pubsub_topic          = "{{task_pubsub_topic}}"
message_retention_duration = "{{pubsub_message_retention_duration}}"
eventarc_trigger_name      = "{{eventarc_trigger_name}}"
eventarc_cloudrun_service  = "{{eventarc_cloudrun_service}}"
eventarc_gke_cluster       = "{{eventarc_gke_cluster}}"
eventarc_gke_namespace     = "{{eventarc_gke_namespace}}"
eventarc_gke_path          = "{{eventarc_gke_path}}"
eventarc_gke_service       = "{{eventarc_gke_service}}"
