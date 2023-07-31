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
  vpc_network               = data.terraform_remote_state.foundation.outputs.vpc_network
  vpc_subnetwork            = data.terraform_remote_state.foundation.outputs.vpc_subnetwork
  ip_cidr_range             = data.terraform_remote_state.foundation.outputs.ip_cidr_range
  secondary_ranges_pods     = data.terraform_remote_state.foundation.outputs.secondary_ranges_pods
  secondary_ranges_services = data.terraform_remote_state.foundation.outputs.secondary_ranges_services
  master_ipv4_cidr_block    = data.terraform_remote_state.foundation.outputs.master_ipv4_cidr_block
}

data "google_project" "project" {}


data "terraform_remote_state" "foundation" {
  backend = "gcs"
  config = {
    bucket = "${var.project_id}-tfstate"
    prefix = "stage/2-foundation"
  }
}

module "gke" {
  source                    = "../../modules/gke"
  project_id                = var.project_id
  cluster_name              = var.cluster_name
  namespace                 = "default"
  vpc_network               = local.vpc_network
  vpc_subnetwork            = local.vpc_subnetwork
  region                    = var.region
  secondary_ranges_pods     = local.secondary_ranges_pods
  secondary_ranges_services = local.secondary_ranges_services
  master_ipv4_cidr_block    = local.master_ipv4_cidr_block
  enable_private_nodes      = var.private_cluster
  min_node_count            = 1
  max_node_count            = 10
  machine_type              = var.node_machine_type

  # This service account will be created in both GCP and GKE, and will be
  # used for workload federation in all microservices.
  # See microservices/sample_service/kustomize/base/deployment.yaml for example.
  service_account_name = "gke-sa"

  # See latest stable version at https://cloud.google.com/kubernetes-engine/docs/release-notes-stable
  kubernetes_version = var.kubernetes_version
}
