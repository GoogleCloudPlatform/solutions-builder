/**
 * Copyright 2022 Google LLC
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

resource "google_project_iam_member" "cloudbuild-sa-iam" {
  for_each = toset([
    "roles/compute.admin",
    "roles/compute.serviceAgent",
    "roles/eventarc.admin",
    "roles/eventarc.eventReceiver",
    "roles/eventarc.serviceAgent",
    "roles/iam.serviceAccountTokenCreator",
    "roles/iam.serviceAccountUser",
    "roles/run.admin",
    "roles/run.invoker",
    "roles/serviceusage.serviceUsageConsumer",
    "roles/storage.admin",
  ])
  role    = each.key
  member  = "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
  project = var.project_id
}

resource "google_project_iam_member" "default-compute-sa-iam" {
  for_each = toset([
    "roles/compute.admin",
    "roles/compute.serviceAgent",
    "roles/eventarc.admin",
    "roles/eventarc.eventReceiver",
    "roles/eventarc.serviceAgent",
    "roles/iam.serviceAccountTokenCreator",
    "roles/iam.serviceAccountUser",
    "roles/run.admin",
    "roles/run.invoker",
    "roles/serviceusage.serviceUsageConsumer",
    "roles/storage.admin",
  ])
  role    = each.key
  member  = "serviceAccount:${var.project_number}-compute@developer.gserviceaccount.com"
  project = var.project_id
}

module "service_accounts" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 3.0"
  project_id   = var.project_id
  names        = ["deployment-${var.env}"]
  display_name = "deployment-${var.env}"
  description  = "Deployment SA for ${var.env}"
  project_roles = [for i in [
    "roles/aiplatform.admin",
    "roles/artifactregistry.admin",
    "roles/cloudbuild.builds.builder",
    "roles/cloudtrace.agent",
    "roles/compute.admin",
    "roles/container.admin",
    "roles/containerregistry.ServiceAgent",
    "roles/datastore.owner",
    "roles/firebase.admin",
    "roles/iam.serviceAccountTokenCreator",
    "roles/iam.serviceAccountUser",
    "roles/iam.workloadIdentityUser",
    "roles/logging.admin",
    "roles/logging.viewer",
    "roles/run.admin",
    "roles/secretmanager.secretAccessor",
    "roles/storage.admin",
    "roles/viewer",
  ] : "${var.project_id}=>${i}"]
  generate_keys = false
}
