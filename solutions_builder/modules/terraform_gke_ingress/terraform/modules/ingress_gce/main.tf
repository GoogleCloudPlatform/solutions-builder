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

# Terraform Block
terraform {
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.7.0"
    }
  }
}

locals {
  global_static_ip_name = (
    var.external_ip_address != null ? var.external_ip_address
    : google_compute_global_address.ingress_ip_address[0].name
  )
}

resource "google_compute_global_address" "ingress_ip_address" {
  count        = var.external_ip_address == null ? 1 : 0
  project      = var.project_id
  name         = "gke-ingress-ip"
  address_type = "EXTERNAL"
}

resource "google_compute_managed_ssl_certificate" "managed_certificate" {
  provider = google-beta

  name = var.managed_cert_name
  managed {
    domains = var.domains
  }
}

resource "google_compute_ssl_policy" "gke-ingress-ssl-policy" {
  name            = "gke-ingress-ssl-policy"
  profile         = "MODERN"
  min_tls_version = "TLS_1_2"
}
