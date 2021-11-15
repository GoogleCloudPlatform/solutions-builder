terraform {
  required_providers {
    google = {
      version = "~>4.0"
    }
  }
}

provider "google" {
  project = var.project_id
}

data "google_client_config" "access_token" {}

provider "kubernetes" {
  host                   = google_container_cluster.main-cluster.endpoint
  token                  = data.google_client_config.access_token.access_token
  client_certificate     = base64decode(google_container_cluster.main-cluster.master_auth.0.client_certificate)
  client_key             = base64decode(google_container_cluster.main-cluster.master_auth.0.client_key)
  cluster_ca_certificate = base64decode(google_container_cluster.main-cluster.master_auth.0.cluster_ca_certificate)
}
