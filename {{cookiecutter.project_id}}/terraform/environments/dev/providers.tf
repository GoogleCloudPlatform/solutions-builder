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

# Terraform Block
terraform {
  required_version = ">= 0.13"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>4.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.5.1"
    }
  }
}

provider "google" {
  project = var.project_id
}

data "google_client_config" "default" {}

# Defer reading the cluster data until the GKE cluster exists.
data "google_container_cluster" "default" {
  # as-is this will probably need to be run a few times
  name     = "main-cluster"
  location = var.region
  project  = var.project_id
}

# Used by module.gke.
provider "kubernetes" {
  host  = data.google_container_cluster.default.endpoint
  token = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(
    try(data.google_container_cluster.default.master_auth[0].cluster_ca_certificate, ""),
  )
}

# Used by module.ingress.
provider "kubectl" {
  host  = data.google_container_cluster.default.endpoint
  token = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(
    try(data.google_container_cluster.default.master_auth[0].cluster_ca_certificate, ""),
  )
}

provider "helm" {
  kubernetes {
    host  = data.google_container_cluster.default.endpoint
    token = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(
      try(data.google_container_cluster.default.master_auth[0].cluster_ca_certificate, ""),
    )
  }
}
