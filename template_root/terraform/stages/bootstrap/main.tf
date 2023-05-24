locals {
  services = [
    "cloudresourcemanager.googleapis.com", # Cloud Resource Manager
    "cloudbilling.googleapis.com",         # Cloud Billing
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
resource "time_sleep" "wait_90_seconds" {
  depends_on = [google_project_service.project-apis]
  create_duration = "90s"
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
