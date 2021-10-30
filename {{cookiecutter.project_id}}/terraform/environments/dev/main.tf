# project-specific locals
locals {
  env              = var.env
  #TODO: change
  region           = var.region
  firestore_region = var.firestore_region
  multiregion      = var.multiregion
  project_id       = var.project_id
  services = [
    "appengine.googleapis.com",            # AppEngine
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
    "secretmanager.googleapis.com",        # Secret Manager
    "storage.googleapis.com",              # Cloud Storage
  ]
}


resource "google_project_service" "project-apis" {
  for_each                   = toset(local.services)
  project                    = local.project_id
  service                    = each.value
  disable_dependent_services = true
}

module "gke-pod-service-account" {
  source       = "github.com/terraform-google-modules/cloud-foundation-fabric/modules/iam-service-account/"
  project_id   = local.project_id
  name         = "${local.project_id}-sa-${local.env}"
  display_name = "The GKE Pod worker service account. Most microservices run as this."

  # authoritative roles granted *on* the service accounts to other identities
  iam = {
    "roles/iam.serviceAccountUser" = []
  }
  # non-authoritative roles granted *to* the service accounts on other resources
  iam_project_roles = {
    (local.project_id) = [
      "roles/firebase.admin",
      "roles/bigquery.admin",
      "roles/datastore.owner",
      "roles/datastore.importExportAdmin",
      "roles/storage.objectAdmin",
      "roles/storage.admin",
      "roles/secretmanager.secretAccessor",
      # Granting Workload Identity User to SA for GKE -> CloudSQL requests
      "roles/iam.workloadIdentityUser",
      # Granting Dataflow Admin and Dataflow Worker for Fraud Jobs
      "roles/dataflow.admin",
      "roles/dataflow.worker",
    ]
  }
}


module "gke-node-service-account" {
  source       = "github.com/terraform-google-modules/cloud-foundation-fabric/modules/iam-service-account/"
  project_id   = local.project_id
  name         = "${local.project_id}-gke-sa-${local.env}"
  display_name = "This service acount authenticates GKE cluster's access to logging, monitoring and storage services."

  # authoritative roles granted *on* the service accounts to other identities
  iam = {
    "roles/iam.serviceAccountUser" = []
  }
  # non-authoritative roles granted *to* the service accounts on other resources
  iam_project_roles = {
    (local.project_id) = [
      "roles/monitoring.viewer",
      "roles/monitoring.metricWriter",
      "roles/logging.logWriter",
      "roles/stackdriver.resourceMetadata.writer",
      "roles/storage.admin",
      "roles/containerregistry.ServiceAgent",
    ]
  }
}

module "cicd-terraform-account" {
  source       = "github.com/terraform-google-modules/cloud-foundation-fabric/modules/iam-service-account/"
  project_id   = local.project_id
  name         = "tf-${local.project_id}-${local.env}"
  display_name = "The Terraform Service Account. Used by CICD processes."

  # authoritative roles granted *on* the service accounts to other identities
  iam = {
    "roles/iam.serviceAccountUser" = []
  }
  # non-authoritative roles granted *to* the service accounts on other resources
  iam_project_roles = {
    (local.project_id) = [
      "roles/storage.admin",
      "roles/compute.instanceAdmin",
      "roles/iam.serviceAccountAdmin",
      "roles/secretmanager.admin",
      "roles/container.admin",
      "roles/iam.securityAdmin",
      "roles/compute.networkAdmin",
      "roles/appengine.appAdmin",
      "roles/dataflow.admin",
      # needed to create firestore
      # "roles/owner",
    ]
  }
}

resource "google_container_cluster" "main-cluster" {
  depends_on = [google_project_service.project-apis]
  name     = "default-cluster"
  location = local.region
  # networking_mode = "VPC_NATIVE"

  #to enable VPC native
  # ip_allocation_policy {
  #   cluster_secondary_range_name  = google_compute_subnetwork.gke-pods.name
  #   services_secondary_range_name = google_compute_subnetwork.gke-services.name
  # }

  workload_identity_config {
    workload_pool = "${local.project_id}.svc.id.goog"
  }

  #to enable private GKE nodes
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "10.0.1.0/28"
    master_global_access_config {
      #Without this terraform wont be able to deploy applications from local terminal.
      #Advanced users can disable this and run terraform from an instance inside the VPC with CIDR whitelisted in master authorized networks
      enabled = true
    }
  }

  min_master_version = "1.21"
  release_channel {
    channel = "RAPID"
  }

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_nodes" {
  name              = "primary-node-pool"
  location          = local.region
  cluster           = google_container_cluster.main-cluster.name
  node_count        = 1
  max_pods_per_node = 25

  node_config {
    machine_type = "n1-standard-8"
    tags = [
      "${local.project_id}-${local.env}-gke-nodes",
      "allow-health-checks",
    ]

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = module.gke-node-service-account.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  upgrade_settings {
    max_surge       = 3
    max_unavailable = 0
  }
}


# Creating a Kubernetes Service account for Workload Identity
resource "kubernetes_service_account" "ksa" {
  metadata {
    name = "ksa"
    annotations = {
      "iam.gke.io/gcp-service-account" = module.gke-pod-service-account.email
    }
  }
}

# Enable the IAM binding between your YOUR-GSA-NAME and YOUR-KSA-NAME:
resource "google_service_account_iam_binding" "gsa-ksa-binding" {
  service_account_id = module.gke-pod-service-account.service_account.id
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "serviceAccount:${local.project_id}.svc.id.goog[default/ksa]"
  ]

  depends_on = [kubernetes_service_account.ksa]
}

# Instantiate firestore on environment
resource "google_app_engine_application" "firestore" {
  provider      = google
  location_id   = local.firestore_region
  database_type = "CLOUD_FIRESTORE"
}

resource "google_storage_bucket" "default" {
  name          = "${local.project_id}"
  location      = local.multiregion
  storage_class = "STANDARD"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "assets" {
  name          = "${local.project_id}-assets"
  location      = local.multiregion
  storage_class = "STANDARD"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "firestore-backup-bucket" {
  name          = "${local.project_id}-firestore-backup"
  location      = local.multiregion
  storage_class = "NEARLINE"

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 356
    }
    action {
      type = "Delete"
    }
  }
}

# give backup SA rights on bucket
resource "google_storage_bucket_iam_binding" "firestore_sa_backup_binding" {
  bucket = google_storage_bucket.firestore-backup-bucket.name
  role   = "roles/storage.admin"
  members = [
    "serviceAccount:${local.project_id}@appspot.gserviceaccount.com",
  ]
  depends_on = [
    google_app_engine_application.firestore
  ]
}

resource "google_compute_router" "router" {
  name    = "${local.project_id}-router"
  region  = local.region
  network = google_container_cluster.main-cluster.network

  bgp {
    asn = 64514
  }
}

resource "google_compute_router_nat" "nat" {
  name                               = "router-nat"
  router                             = google_compute_router.router.name
  region                             = google_compute_router.router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}
