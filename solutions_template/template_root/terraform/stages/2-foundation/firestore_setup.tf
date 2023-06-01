variable "firestore_region" {
  type        = string
  description = "Firestore Region"
  default     = "us-central"
}

variable "existing_firestore_name" {
  type        = string
  description = "Does this project has existing firestore?"
  default     = "{{project_id | get_existing_firestore}}"
}

module "firebase" {
  source           = "../../modules/firebase"
  project_id       = var.project_id
  firestore_region = var.firestore_region
  firebase_init    = var.existing_firestore_name == "" ? true : false
}
