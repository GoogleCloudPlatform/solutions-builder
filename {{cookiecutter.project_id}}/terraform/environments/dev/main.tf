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

module "project_services" {
  source     = "../../modules/project_services"
  project_id = var.project_id
  services   = local.services
}

module "service_accounts" {
  depends_on = [module.project_services]
  source     = "../../modules/service_accounts"
  project_id = var.project_id
  env        = var.env
}

module "vpc_network" {
  source      = "../../modules/vpc_network"
  project_id  = var.project_id
  vpc_network = "default-vpc"
  region      = var.region
}

module "gke" {
  depends_on = [module.project_services, module.vpc_network]

  # Only execute this module when feature_flags contains the keyword.
  count = (contains(regexall("[\\w\\d\\-_\\+\\.]+", var.feature_flags), "gke") ? 1 : 0)

  source         = "../../modules/gke"
  project_id     = var.project_id
  cluster_name   = "main-cluster"
  vpc_network    = "default-vpc"
  region         = var.region
  min_node_count = 1
  max_node_count = 1
  machine_type   = "n1-standard-8"
}

module "ingress" {
  depends_on = [module.gke]

  # Only execute this module when feature_flags contains the keyword.
  count = (contains(regexall("[\\w\\d\\-_\\+\\.]+", var.feature_flags), "gke-ingress") ? 1 : 0)

  source            = "../../modules/ingress"
  project_id        = var.project_id
  cert_issuer_email = var.admin_email

  # Domains for API endpoint, excluding protocols.
  domain            = var.api_domain
  region            = var.region
  cors_allow_origin = "http://localhost:4200,http://localhost:3000,${var.web_app_domain}"
}

module "firebase" {
  source           = "../../modules/firebase"
  project_id       = var.project_id
  firestore_region = var.firestore_region
}

module "cloudrun" {
  depends_on = [module.project_services, module.vpc_network]
  source     = "../../modules/cloudrun"
  project_id = var.project_id
  region     = var.region
  services   = [
    "cloudrun-sample"
  ]
}
