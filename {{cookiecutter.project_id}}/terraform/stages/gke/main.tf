/**
 * Copyright 2022 Google LLC
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

# project-specific locals
locals {
  lh = join("", ["local", "host"])
}

data "google_project" "project" {}

module "gke" {
  source         = "../../modules/gke"
  project_id     = var.project_id
  cluster_name   = "main-cluster"
  namespace      = "default"
  vpc_network    = "default-vpc"
  region         = var.region
  min_node_count = 1
  max_node_count = 10
  machine_type   = "n1-standard-8"

  # This service account will be created in both GCP and GKE, and will be
  # used for workload federation in all microservices.
  # See microservices/sample_service/kustomize/base/deployment.yaml for example.
  service_account_name = "gke-sa"

  # See latest stable version at https://cloud.google.com/kubernetes-engine/docs/release-notes-stable
  kubernetes_version = "1.23.13-gke.900"
}

module "ingress" {
  depends_on = [module.gke]

  source            = "../../modules/ingress"
  project_id        = var.project_id
  cert_issuer_email = var.admin_email
  region            = var.region

  # API domain, excluding protocols. E.g. example.com.
  api_domain        = var.api_domain
  cors_allow_origin = "http://${local.lh}:4200,http://${local.lh}:3000,http://${var.web_app_domain},https://${var.web_app_domain}"
}
