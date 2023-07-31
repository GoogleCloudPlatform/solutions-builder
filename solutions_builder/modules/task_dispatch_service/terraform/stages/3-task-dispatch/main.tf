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

# project-specific locals
locals {
  roles_for_eventarc_sa = [
    "roles/compute.viewer",
    "roles/container.developer",
    "roles/iam.serviceAccountAdmin",
    "roles/eventarc.admin",
    "roles/eventarc.eventReceiver",
    "roles/eventarc.serviceAgent",
  ]
}

# Used to retrieve project_number later
data "google_project" "project" {
}

resource "google_pubsub_topic" "task_pubsub_topic" {
  name                       = var.task_pubsub_topic
  message_retention_duration = var.message_retention_duration
}

# Add IAM roles for EventArc service agent.
resource "google_project_iam_member" "eventarc_sa_iam" {
  for_each   = toset(local.roles_for_eventarc_sa)
  role       = each.key
  member     = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-eventarc.iam.gserviceaccount.com"
  project    = var.project_id
}

resource "null_resource" "eventarc_enable_gke_destination" {
  depends_on = [
    google_project_iam_member.eventarc_sa_iam
  ]

  provisioner "local-exec" {
    command = "printf 'yes' | gcloud eventarc gke-destinations init --project=${var.project_id}"
  }
}

# Create a Pub/Sub trigger
resource "google_eventarc_trigger" "task_pubsub_trigger" {
  depends_on = [
    null_resource.eventarc_enable_gke_destination,
    google_pubsub_topic.task_pubsub_topic
  ]
  name     = var.eventarc_trigger_name
  location = var.region

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.pubsub.topic.v1.messagePublished"
  }
  destination {
    {% if default_deploy == "cloudrun" -%} cloud_run_service {
      service = var.eventarc_cloudrun_service
      region  = var.region
    }{%- endif %}

    {% if default_deploy == "gke" -%} gke {
      cluster   = var.eventarc_gke_cluster
      location  = var.region
      namespace = var.eventarc_gke_namespace
      path      = var.eventarc_gke_path
      service   = var.eventarc_gke_service
    }{%- endif %}
  }

  service_account = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"

  transport {
    pubsub {
      topic = var.task_pubsub_topic
    }
  }
}

