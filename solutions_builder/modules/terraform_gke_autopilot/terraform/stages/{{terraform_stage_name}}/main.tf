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
  vpc_network          = data.terraform_remote_state.foundation.outputs.vpc_network
  vpc_subnetwork       = data.terraform_remote_state.foundation.outputs.vpc_subnetwork
  service_account_name = "gke-sa"
  default_namespace    = "default"
}

data "google_project" "project" {}

data "terraform_remote_state" "foundation" {
  backend = "gcs"
  config = {
    bucket = "${var.project_id}-tfstate"
    prefix = "stage/2-foundation"
  }
}

resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.region

  network    = local.vpc_network
  subnetwork = local.vpc_subnetwork

  # Enabling Autopilot for this cluster
  enable_autopilot    = true
  deletion_protection = false
}

resource "google_service_account" "service_account" {
  account_id   = local.service_account_name
  display_name = "Service Account for GKE"
}
