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
  project = var.project_id
}

module "gke_cluster" {
  source                            = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  project_id                        = var.project_id
  name                              = var.cluster_name
  kubernetes_version                = var.kubernetes_version
  region                            = var.region
  regional                          = true
  network                           = var.vpc_network
  subnetwork                        = var.vpc_subnetwork
  enable_private_nodes              = var.enable_private_nodes
  master_ipv4_cidr_block            = var.master_ipv4_cidr_block
  ip_range_pods                     = var.secondary_ranges_pods.range_name
  ip_range_services                 = var.secondary_ranges_services.range_name
  add_master_webhook_firewall_rules = true
  http_load_balancing               = true
  identity_namespace                = "enabled"
  horizontal_pod_autoscaling        = true
  remove_default_node_pool          = true

  node_pools = [
    {
      name               = var.node_pool_name
      machine_type       = var.machine_type
      min_count          = var.min_node_count
      max_count          = var.max_node_count
      disk_size_gb       = var.disk_size_gb
      disk_type          = "pd-standard"
      image_type         = "COS_CONTAINERD"
      auto_repair        = true
      auto_upgrade       = true
      preemptible        = false
      initial_node_count = "1"
      enable_secure_boot = true
      node_locations     = var.node_locations

      # hard coding until resolved: https://github.com/terraform-google-modules/terraform-google-kubernetes-engine/issues/991
      service_account = "${var.service_account_name}@${var.project_id}.iam.gserviceaccount.com"
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
  depends_on      = [module.gke_cluster]
  create_duration = "120s"
}

module "cloud-nat" {
  count                              = var.enable_private_nodes ? 1 : 0
  source                             = "terraform-google-modules/cloud-nat/google"
  version                            = "~> 1.2"
  name                               = format("%s-%s-gke-nat", var.project_id, var.region)
  create_router                      = true
  router                             = format("%s-%s-gke-router", var.project_id, var.region)
  project_id                         = var.project_id
  region                             = var.region
  network                            = var.vpc_network
  source_subnetwork_ip_ranges_to_nat = var.source_subnetwork_ip_ranges_to_nat
  log_config_enable                  = true
  log_config_filter                  = "ERRORS_ONLY"
}

module "gke-workload-identity" {
  source     = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
  name       = var.service_account_name
  namespace  = var.namespace
  project_id = var.project_id
  roles      = var.gke_service_account_roles
}
