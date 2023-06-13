locals {
  services = [
    "cloudresourcemanager.googleapis.com", # Cloud Resource Manager
    "cloudbilling.googleapis.com",         # Cloud Billing
    "cloudbuild.googleapis.com",           # Cloud Build
    "serviceusage.googleapis.com",         # Service Usage
    "storage.googleapis.com",              # Service Usage
  ]
}

# basic APIs needed to get project up and running
resource "google_project_service" "project-apis" {
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.value
  disable_dependent_services = true
}

# add timer to avoid errors on new project creation and API enables
resource "time_sleep" "wait_60_seconds" {
  depends_on = [google_project_service.project-apis]
  create_duration = "60s"
}

module "terraform_runner_service_account" {
  depends_on   = [time_sleep.wait_60_seconds]
  source       = "../../modules/service_account"
  project_id   = var.project_id
  name         = "terraform-runner"
  display_name = "terraform-runner"
  description  = "Service Account for Terraform"
  roles = [
    "roles/aiplatform.admin",
    "roles/artifactregistry.admin",
    "roles/cloudbuild.builds.builder",
    "roles/cloudtrace.agent",
    "roles/compute.admin",
    "roles/container.admin",
    "roles/containerregistry.ServiceAgent",
    "roles/datastore.owner",
    "roles/editor",
    "roles/firebase.admin",
    "roles/iam.serviceAccountTokenCreator",
    "roles/iam.serviceAccountUser",
    "roles/iam.workloadIdentityUser",
    "roles/iam.workloadIdentityUser",
    "roles/logging.admin",
    "roles/logging.viewer",
    "roles/resourcemanager.projectIamAdmin",
    "roles/run.admin",
    "roles/secretmanager.secretAccessor",
    "roles/storage.admin",
  ]
}

{% if terraform_backend_gcs == true -%}
resource "google_storage_bucket" "tfstate-bucket" {
  name                        = "${var.project_id}-tfstate"
  location                    = var.storage_multiregion
  project                     = var.project_id
  force_destroy               = false
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}
{%- endif %}
