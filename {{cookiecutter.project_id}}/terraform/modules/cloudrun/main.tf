resource "google_artifact_registry_repository" "cloudrun_repository" {
  location      = var.region
  repository_id = "cloudrun"
  description   = "Docker repository for CloudRun"
  format        = "DOCKER"
}

resource "google_cloud_run_service_iam_member" "member" {
  for_each = toset(var.services)
  project  = var.project_id
  location = var.region
  service  = each.value
  role     = "roles/run.invoker"
  member   = "allUsers"
}
