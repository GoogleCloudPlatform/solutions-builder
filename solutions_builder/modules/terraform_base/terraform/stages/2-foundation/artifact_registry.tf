resource "google_artifact_registry_repository" "default" {
  location      = var.artifact_registry_region
  repository_id = "default"
  description   = "Default docker repository"
  format        = "DOCKER"
}
