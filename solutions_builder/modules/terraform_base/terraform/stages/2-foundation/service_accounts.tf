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
  roles_for_default_sa = [
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
  ]
}


resource "google_project_iam_member" "cloudbuild-sa-iam" {
  depends_on = [module.project_services]
  for_each   = toset(local.roles_for_default_sa)
  role       = each.key
  member     = "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
  project    = var.project_id
}

resource "google_project_iam_member" "default-compute-sa-iam" {
  depends_on = [module.project_services]
  for_each   = toset(local.roles_for_default_sa)
  role       = each.key
  member     = "serviceAccount:${var.project_number}-compute@developer.gserviceaccount.com"
  project    = var.project_id
}

module "deployment_service_account" {
  depends_on   = [module.project_services]
  source       = "../../modules/service_account"
  project_id   = var.project_id
  name         = "deployment"
  display_name = "deployment"
  description  = "Service Account for deployment"
  roles        = roles_for_default_sa
}
