/**
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

variable "firestore_region" {
  type        = string
  description = "Firestore Region"
  default     = "us-central"
}

variable "existing_firestore_name" {
  type        = string
  description = "Does this project has existing firestore?"
  default     = ""
}

module "firebase" {
  source           = "../../modules/firebase"
  project_id       = var.project_id
  firestore_region = var.firestore_region
  firebase_init    = var.existing_firestore_name == "" ? true : false
}

resource "google_project_service" "firestore" {
  project = var.project_id
  service = "firestore.googleapis.com"
}

resource "google_firestore_database" "database" {
  depends_on = [google_project_service.firestore]

  project     = var.project_id
  location_id = var.firestore_location_id
  name        = "(default)"
  type        = "FIRESTORE_NATIVE"
}
