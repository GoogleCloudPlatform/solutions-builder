variable "project_id" {
  type        = string
  description = "project ID"
}

variable "firestore_region" {
  type        = string
  description = "Firestore Region - must be app_engine region"
  # options for firestore: https://cloud.google.com/appengine/docs/locations
  # {{cookiecutter.gcp_region}} and europe-west1 must be us-central and europe-west for legacy reasons
  default = "us-central"
}

variable "storage_multiregion" {
  type    = string
  default = "us"
}
