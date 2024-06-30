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
  services = [
    "aiplatform.googleapis.com",           # Vertex AI
    "apikeys.googleapis.com",              # API Keys
    "appengine.googleapis.com",            # AppEngine
    "artifactregistry.googleapis.com",     # Artifact Registry
    "bigquery.googleapis.com",             # BigQuery
    "bigquerydatatransfer.googleapis.com", # BigQuery Data Transfer
    "cloudbuild.googleapis.com",           # Cloud Build
    "container.googleapis.com",            # Google Kubernetes Engine
    "containerregistry.googleapis.com",    # Google Container Registry
    "dataflow.googleapis.com",             # Cloud Dataflow
    "eventarc.googleapis.com",             # Event Arc
    "firebase.googleapis.com",             # Firebase
    "firestore.googleapis.com",            # Firestore
    "iam.googleapis.com",                  # Cloud IAM
    "identitytoolkit.googleapis.com",      # Identity Toolkit
    "iap.googleapis.com",                  # Idenity-aware proxy
    "logging.googleapis.com",              # Cloud Logging
    "monitoring.googleapis.com",           # Cloud Operations Suite
    "pubsub.googleapis.com",               # Pub/Sub
    "run.googleapis.com",                  # Cloud Run
    "secretmanager.googleapis.com",        # Secret Manager
    "storage.googleapis.com",              # Cloud Storage
  ]
}

# Used to retrieve project_number later
data "google_project" "project" {}

module "project_services" {
  source     = "../../modules/project_services"
  project_id = var.project_id
  services   = local.services
}

module "vpc_network" {
  count                     = ((var.vpc_network != null && var.vpc_network != "") ? 1 : 0)
  depends_on                = [module.project_services]
  source                    = "../../modules/vpc_network"
  project_id                = var.project_id
  vpc_network               = var.vpc_network
  region                    = var.region
  vpc_subnetwork            = var.vpc_subnetwork
  subnet_ip                 = var.ip_cidr_range
  secondary_ranges_pods     = var.secondary_ranges_pods
  secondary_ranges_services = var.secondary_ranges_services
}
