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

# Used by module.gke.
provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

# Used by module.ingress.
provider "kubectl" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
  load_config_file       = false
}

provider "helm" {
  kubernetes {
    host                   = "https://${module.gke.endpoint}"
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(module.gke.ca_certificate)
  }
}

provider "google" {
  project = var.project_id
}

# Terraform Block
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.50.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.7.0"
    }
  }
}

data "google_client_config" "default" {}

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

# Variables

variable "project_id" {
  type        = string
  description = "GCP Project ID"

  validation {
    condition     = length(var.project_id) > 0
    error_message = "The project_id value must be an non-empty string."
  }
}

variable "region" {
  type        = string
  description = "Default GCP region"
  default     = "us-central1"

  validation {
    condition     = length(var.region) > 0
    error_message = "The region value must be an non-empty string."
  }
}

variable "cluster_name" {
  type    = string
  default = "main-cluster"
}

variable "kubernetes_version" {
  type        = string
  description = "Kubernetes version. See https://cloud.google.com/kubernetes-engine/docs/release-notes-stable"
}

variable "node_machine_type" {
  type        = string
  description = "VM machine time"
  default     = "n2-standard-2"
}

variable "private_cluster" {
  type        = bool
  description = "Whether to use private nodes"
  default     = true
}
