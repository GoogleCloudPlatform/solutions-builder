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
    "compute.googleapis.com",              # Load Balancers, Cloud Armor
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

module "firebase" {
  depends_on       = [module.project_services]
  source           = "../../modules/firebase"
  project_id       = var.project_id
  firestore_region = var.firestore_region
  firebase_init    = var.firebase_init
}

module "vpc_network" {
  source      = "../../modules/vpc_network"
  project_id  = var.project_id
  vpc_network = "default-vpc"
  region      = var.region
}

module "gke" {
  depends_on = [module.project_services, module.vpc_network]

  source         = "../../modules/gke"
  project_id     = var.project_id
  cluster_name   = "main-cluster"
  namespace      = "default"
  vpc_network    = "default-vpc"
  region         = var.region
  min_node_count = 1
  max_node_count = 10
  machine_type   = "n1-standard-8"

  # This service account will be created in both GCP and GKE, and will be
  # used for workload federation in all microservices.
  # See microservices/sample_service/kustomize/base/deployment.yaml for example.
  service_account_name = "gke-sa"

  # See latest stable version at https://cloud.google.com/kubernetes-engine/docs/release-notes-stable
  kubernetes_version = "1.23.13-gke.900"
}

module "ingress" {
  depends_on = [module.gke]

  source            = "../../modules/ingress"
  project_id        = var.project_id
  cert_issuer_email = var.admin_email
  region            = var.region

  # API domain, excluding protocols. E.g. example.com.
  api_domain        = var.api_domain
  cors_allow_origin = "http://localhost:4200,http://localhost:3000,http://${var.web_app_domain},https://${var.web_app_domain}"
}

# # [Optional] Deploy sample-service to CloudRun
# # Uncomment below to enable deploying microservices with CloudRun.
# module "cloudrun-sample" {
#   depends_on = [module.project_services, module.vpc_network]

#   source                = "../../modules/cloudrun"
#   project_id            = var.project_id
#   region                = var.region
#   source_dir            = "../../../microservices/sample_service"
#   service_name          = "cloudrun-sample"
#   repository_id         = "cloudrun"
#   allow_unauthenticated = true
# }
