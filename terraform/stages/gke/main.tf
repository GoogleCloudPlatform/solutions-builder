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

# project-specific locals
locals {
  lh             = join("", ["local", "host"])
  vpc_network    = data.terraform_remote_state.foundation.outputs.vpc_network
  vpc_network_id = data.terraform_remote_state.foundation.outputs.vpc_network_id
  api_domain     = data.terraform_remote_state.foundation.outputs.api_domain
  admin_email    = data.terraform_remote_state.foundation.outputs.admin_email
}

data "google_project" "project" {}

data "terraform_remote_state" "foundation" {
  backend = "gcs"
  config = {
    bucket = "${var.project_id}-tfstate"
    prefix = "stage/foundation"
  }
}

resource "google_compute_subnetwork" "subnetwork" {
  name                     = var.vpc_subnetwork
  ip_cidr_range            = var.ip_cidr_range
  region                   = var.region
  network                  = local.vpc_network_id
  private_ip_google_access = true

  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.7
    metadata             = "INCLUDE_ALL_METADATA"
  }

  secondary_ip_range = [
    var.secondary_ranges_pods,
    var.secondary_ranges_services
  ]
}

module "gke" {
  depends_on                = [google_compute_subnetwork.subnetwork]
  source                    = "../../modules/gke"
  project_id                = var.project_id
  cluster_name              = var.cluster_name
  namespace                 = "default"
  vpc_network               = local.vpc_network
  vpc_subnetwork            = var.vpc_subnetwork
  region                    = var.region
  secondary_ranges_pods     = var.secondary_ranges_pods
  secondary_ranges_services = var.secondary_ranges_services
  master_ipv4_cidr_block    = var.master_ipv4_cidr_block
  enable_private_nodes      = true
  min_node_count            = 1
  max_node_count            = 10
  machine_type              = "n1-standard-4"

  # This service account will be created in both GCP and GKE, and will be
  # used for workload federation in all microservices.
  # See microservices/sample_service/kustomize/base/deployment.yaml for example.
  service_account_name = "gke-sa"

  # See latest stable version at https://cloud.google.com/kubernetes-engine/docs/release-notes-stable
  kubernetes_version = "1.23.16-gke.1400"
}

module "ingress" {
  depends_on = [module.gke]

  source            = "../../modules/ingress_nginx"
  project_id        = var.project_id
  cert_issuer_email = local.admin_email
  region            = var.region

  # API domain, excluding protocols. E.g. example.com.
  api_domain        = local.api_domain
  cors_allow_origin = "http://${local.lh}:4200,http://${local.lh}:3000,http://${var.web_app_domain},https://${var.web_app_domain}"
}
