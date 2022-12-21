# Enabling a firbase project

resource "google_app_engine_application" "firebase_init" {
  # Only execute this module when global var firebase_init set as "true"
  # NOTE: the Firebase can only be initialized once (via App Engine).
  count = var.firebase_init ? 1 : 0

  provider      = google-beta
  project       = var.project_id
  location_id   = var.firestore_region
  database_type = "CLOUD_FIRESTORE"
}

resource "google_storage_bucket" "firestore-backup-bucket" {
  name          = "${var.project_id}-firestore-backup"
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

# main service account to be used by kubernetes pods running the aplpications
module "firebase_backup_sa" {
  source       = "terraform-google-modules/service-accounts/google"
  version      = "~> 3.0"
  project_id   = var.project_id
  names        = ["firebase-backup"]
  display_name = "Firebase backup service account"
  description  = "Service account for Firestore"
  project_roles = [for i in [
    "roles/datastore.owner",
    "roles/firebase.admin",
    "roles/logging.admin",
    "roles/secretmanager.secretAccessor",
    "roles/storage.admin",
  ] : "${var.project_id}=>${i}"]
  generate_keys = false
}

# give backup SA rights on bucket
resource "google_storage_bucket_iam_binding" "firestore_sa_backup_binding" {
  bucket = google_storage_bucket.firestore-backup-bucket.name
  role   = "roles/storage.admin"
  members = [
    "serviceAccount:firebase-backup@${var.project_id}.iam.gserviceaccount.com",
  ]
  depends_on = [
    module.firebase_backup_sa,
    google_storage_bucket.firestore-backup-bucket
  ]
}
