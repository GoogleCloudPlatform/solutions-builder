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

locals {
  services = [
    "appengine.googleapis.com",            # App Engine
    "cloudresourcemanager.googleapis.com", # Cloud Resource Manager
    "cloudbilling.googleapis.com",         # Cloud Billing
    "cloudbuild.googleapis.com",           # Cloud Build
    "serviceusage.googleapis.com",         # Service Usage
    "storage.googleapis.com",              # Storage Usage
    "iam.googleapis.com",                  # IAM service
  ]
}

# basic APIs needed to get project up and running
resource "google_project_service" "project-apis" {
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.value
  disable_dependent_services = true
}

# add timer to avoid errors on new project creation and API enables
resource "time_sleep" "wait_60_seconds" {
  depends_on      = [google_project_service.project-apis]
  create_duration = "60s"
}

module "terraform_runner_service_account" {
  depends_on   = [time_sleep.wait_60_seconds]
  source       = "../../modules/service_account"
  project_id   = var.project_id
  name         = "terraform-runner"
  display_name = "terraform-runner"
  description  = "Service Account for Terraform"
  roles = [
    "roles/appengine.appAdmin",
    "roles/aiplatform.admin",
    "roles/artifactregistry.admin",
    "roles/cloudbuild.builds.builder",
    "roles/cloudtrace.agent",
    "roles/compute.admin",
    "roles/container.admin",
    "roles/containerregistry.ServiceAgent",
    "roles/datastore.owner",
    "roles/editor",
    "roles/firebase.admin",
    "roles/iam.serviceAccountTokenCreator",
    "roles/iam.serviceAccountUser",
    "roles/iam.workloadIdentityUser",
    "roles/logging.admin",
    "roles/logging.viewer",
    "roles/resourcemanager.projectIamAdmin",
    "roles/run.admin",
    "roles/secretmanager.secretAccessor",
    "roles/storage.admin",
  ]
}

{% if terraform_backend_gcs == true -%}
resource "google_storage_bucket" "tfstate-bucket" {
  name                        = "${var.project_id}-tfstate"
  location                    = var.storage_multiregion
  project                     = var.project_id
  force_destroy               = false
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}
{%- endif %}
