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

module "gke" {
  depends_on = [
    module.service_accounts,
  ]

  source                     = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  version                    = "v22.1.0"
  project_id                 = var.project_id
  name                       = var.cluster_name
  kubernetes_version         = var.kubernetes_version
  region                     = var.region
  regional                   = true
  network                    = var.vpc_network
  subnetwork                 = "vpc-01-subnet-01"
  ip_range_pods              = "secondary-pod-range-01"
  ip_range_services          = "secondary-service-range-01"
  http_load_balancing        = true
  identity_namespace         = "enabled"
  horizontal_pod_autoscaling = true
  remove_default_node_pool   = true

  node_pools = [
    {
      name         = "default-pool"
      machine_type = var.machine_type
      min_count    = var.min_node_count
      max_count    = var.max_node_count
      disk_size_gb = var.disk_size_gb
      disk_type    = "pd-standard"
      image_type   = "COS_CONTAINERD"
      auto_repair  = true
      auto_upgrade = true
      # hard coding until resolved: https://github.com/terraform-google-modules/terraform-google-kubernetes-engine/issues/991
      service_account    = "gke-node-sa@${var.project_id}.iam.gserviceaccount.com"
      preemptible        = false
      initial_node_count = "1"
      enable_secure_boot = true
      node_locations     = var.node_locations
    },
  ]
  node_pools_oauth_scopes = {
    node-pool-01 = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  node_pools_metadata = {
    node-pool-01 = {
      disable-legacy-endpoints = "true"
    }
  }

  node_pools_taints = {
    node-pool-01 = []
  }
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
