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
  services = [
    "appengine.googleapis.com",            # AppEngine
    "artifactregistry.googleapis.com",     # Artifact Registry
    "bigquery.googleapis.com",             # BigQuery
    "bigquerydatatransfer.googleapis.com", # BigQuery Data Transfer
    "cloudbuild.googleapis.com",           # Cloud Build
    "compute.googleapis.com",              # Compute Engine
    "container.googleapis.com",            # Google Kubernetes Engine
    "containerregistry.googleapis.com",    # Google Container Registry
    "dataflow.googleapis.com",             # Cloud Dataflow
    "firebase.googleapis.com",             # Firebase
    "firestore.googleapis.com",            # Firestore
    "iam.googleapis.com",                  # Cloud IAM
    "logging.googleapis.com",              # Cloud Logging
    "monitoring.googleapis.com",           # Cloud Operations Suite
    "run.googleapis.com",                  # Cloud Run
    "secretmanager.googleapis.com",        # Secret Manager
    "storage.googleapis.com",              # Cloud Storage
  ]

  shared_vpc_project = try(var.shared_vpc.host_project, null)
  use_shared_vpc     = var.shared_vpc != null
  region             = (local.use_shared_vpc ? var.shared_vpc.region : var.region)

  network_config = {
    host_project      = (local.use_shared_vpc ? var.shared_vpc.host_project : var.project_id)
    network           = (local.use_shared_vpc ? var.shared_vpc.network : var.vpc_network)
    subnet            = (local.use_shared_vpc ? var.shared_vpc.subnet : var.vpc_subnetwork)
    serverless_subnet = (local.use_shared_vpc ? var.shared_vpc.serverless_subnet : var.serverless_subnet)
    region            = (local.use_shared_vpc ? var.shared_vpc.region : var.region)
  }

}

data "google_project" "project" {}

module "project_services" {
  source     = "../../modules/project_services"
  project_id = var.project_id
  services   = local.services
}

module "service_accounts" {
  depends_on     = [module.project_services]
  source         = "../../modules/service_accounts"
  project_id     = var.project_id
  env            = var.env
  project_number = data.google_project.project.number
}

module "shared_vpc" {
  depends_on        = [module.project_services]
  source            = "../../modules/shared_vpc"
  project_id        = var.project_id
  vpc_network       = var.vpc_network
  region            = var.region
  subnetwork        = var.vpc_subnetwork
  serverless_subnet = var.serverless_subnet
}

module "firebase" {
  depends_on       = [module.project_services]
  source           = "../../modules/firebase"
  project_id       = var.project_id
  firestore_region = var.firestore_region
  firebase_init    = var.firebase_init
}

