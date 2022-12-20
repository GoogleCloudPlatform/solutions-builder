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
}

module "vpc_network" {
  source      = "../../modules/vpc_network"
  project_id  = var.project_id
  vpc_network = "default-vpc"
  region      = var.region
}

# Use GKE autopilot cluster.
module "gke" {
  depends_on = [module.project_services, module.vpc_network]

  source               = "../../modules/gke_autopilot"
  project_id           = var.project_id
  cluster_name         = "main-cluster"
  vpc_network          = "default-vpc"
  vpc_subnetwork       = "default-vpc-subnet"
  namespace            = "default"
  service_account_name = "gke-sa" # This will be used in each microservice.
  region               = var.region

  # See latest stable version at https://cloud.google.com/kubernetes-engine/docs/release-notes-stable
  kubernetes_version = "1.22.12-gke.2300"
}

# # [Optional] Use standard/customize GKE cluster.
# # Comment out the module "gke-autopilot" block out and use the following block to customize GKE cluster with standard mode.

# module "gke" {
#   depends_on = [module.project_services, module.vpc_network]
#   source             = "../../modules/gke"
#   project_id         = var.project_id
#   cluster_name       = "main-cluster"
#   kubernetes_version = "1.22.12-gke.2300"
#   vpc_network        = "default-vpc"
#   region             = var.region
#   min_node_count     = 1
#   max_node_count     = 1
#   machine_type       = "n1-standard-8"
# }

module "gke-ingress" {
  depends_on = [module.gke]

  source            = "../../modules/ingress"
  project_id        = var.project_id
  cert_issuer_email = var.admin_email

  # Domains for API endpoint, excluding protocols.
  domain            = var.api_domain
  region            = var.region
  cors_allow_origin = "http://localhost:4200,http://localhost:3000,http://${var.web_app_domain},https://${var.web_app_domain}"
}

# [Optional] Deploy sample-service to CloudRun
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

