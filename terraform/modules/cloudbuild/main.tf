resource "google_storage_bucket" "cloudbuild-logs" {
  name          = "${var.project_id}-cloudbuild-logs"
  location      = var.storage_multiregion
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
