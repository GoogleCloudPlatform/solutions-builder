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

module "cicd-terraform-account" {
  source       = "github.com/terraform-google-modules/cloud-foundation-fabric.git//modules/iam-service-account"
  project_id   = var.project_id
  name         = "tf-${var.project_id}"
  display_name = "The Terraform Service Account. Used by CICD processes."

  # authoritative roles granted *on* the service accounts to other identities
  iam = {
    "roles/iam.serviceAccountUser" = []
  }
  # non-authoritative roles granted *to* the service accounts on other resources
  iam_project_roles = {
    (var.project_id) = [
      "roles/storage.admin",
      "roles/compute.instanceAdmin",
      "roles/iam.serviceAccountAdmin",
      "roles/secretmanager.admin",
      "roles/container.admin",
      "roles/iam.securityAdmin",
      "roles/compute.networkAdmin",
      "roles/appengine.appAdmin",
      "roles/dataflow.admin",
      # needed to create firestore
      # "roles/owner",
    ]
  }
}
