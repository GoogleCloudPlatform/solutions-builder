locals {
  compute_engine_sa = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

data "google_project" "project" {}

module "service_accounts" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 3.0"
  project_id   = var.project_id
  names        = ["deployment-${var.env}"]
  display_name = "deployment-${var.env}"
  description  = "Deployment SA for ${var.env}"
  project_roles = [for i in [
    "roles/aiplatform.admin",
    "roles/artifactregistry.admin",
    "roles/cloudbuild.builds.builder",
    "roles/cloudtrace.agent",
    "roles/compute.admin",
    "roles/container.admin",
    "roles/containerregistry.ServiceAgent",
    "roles/datastore.owner",
    "roles/firebase.admin",
    "roles/iam.serviceAccountTokenCreator",
    "roles/iam.serviceAccountUser",
    "roles/iam.workloadIdentityUser",
    "roles/logging.admin",
    "roles/logging.viewer",
    "roles/run.admin",
    "roles/secretmanager.secretAccessor",
    "roles/storage.admin",
    "roles/viewer",
  ] : "${var.project_id}=>${i}"]
  generate_keys = false
}

module "cloudbuild_sa_iam_bindings" {
  source  = "terraform-google-modules/iam/google//modules/projects_iam"
  version = "7.4.1"

  projects = [var.project_id]
  mode     = "additive"

  bindings = {
    "roles/run.admin" = [local.compute_engine_sa]
    "roles/iam.serviceAccountUser" = [local.compute_engine_sa]
  }
}
