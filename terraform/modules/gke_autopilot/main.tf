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

locals {
  project = var.project_id
  gke_sa_roles = [
    "roles/aiplatform.user",
    "roles/bigquery.admin",
    "roles/datastore.owner",
    "roles/documentai.admin",
    "roles/firebase.admin",
    "roles/iam.serviceAccountUser",
    "roles/logging.admin",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/pubsub.admin",
    "roles/stackdriver.resourceMetadata.writer",
    "roles/storage.admin",
  ]
  gke_pod_sa_email = "gke-node-sa@${var.project_id}.iam.gserviceaccount.com"
}

module "service_accounts" {
  source        = "terraform-google-modules/service-accounts/google"
  version       = "~> 3.0"
  project_id    = var.project_id
  names         = ["gke-node-sa"]
  display_name  = "SA for GKE Node Pool"
  description   = "Service account is used in the gke node pool"
  project_roles = [for i in local.gke_sa_roles : "${var.project_id}=>${i}"]
}

# GKE cluster
resource "google_container_cluster" "primary" {
  depends_on = [
    module.service_accounts,
  ]

  name     = var.cluster_name
  location = var.region

  network    = var.vpc_network
  subnetwork = var.vpc_subnetwork

  # Enabling Autopilot for this cluster
  enable_autopilot = true
}

resource "time_sleep" "wait_for_gke" {
  depends_on      = [module.gke]
  create_duration = "120s"
}

# Creating a Kubernetes Service account for Workload Identity
resource "kubernetes_service_account" "ksa" {
  depends_on = [module.gke, time_sleep.wait_for_gke]

  metadata {
    name = "ksa"
    annotations = {
      "iam.gke.io/gcp-service-account" = local.gke_pod_sa_email
    }
  }
}

# Enable the IAM binding between YOUR-GSA-NAME and YOUR-KSA-NAME:
resource "google_service_account_iam_binding" "gsa-ksa-binding" {
  depends_on = [module.gke, kubernetes_service_account.ksa]

  service_account_id = "projects/${var.project_id}/serviceAccounts/${local.gke_pod_sa_email}"
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[default/ksa]"
  ]
}
