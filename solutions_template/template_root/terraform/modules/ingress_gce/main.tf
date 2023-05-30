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
  name         = "ingress-ip"
  address_type = "EXTERNAL"
}

resource "google_compute_managed_ssl_certificate" "managed_certificate" {
  provider = google-beta

  name = "${var.cert-name}"
  managed {
    domains = ["${var.domain}"]
  }
}

# resource "kubectl_manifest" "frontend_config" {
#   yaml_body = <<YAML
# apiVersion: networking.gke.io/v1beta1
# kind: FrontendConfig
# metadata:
#   name: ingress-security-config
# spec:
#   sslPolicy: ${google_compute_ssl_policy.gke-ingress-ssl-policy.name}
#   redirectToHttps:
#     enabled: true
# YAML
# }

resource "google_compute_ssl_policy" "gke-ingress-ssl-policy" {
  name            = "gke-ingress-ssl-policy"
  profile         = "MODERN"
  min_tls_version = "TLS_1_2"
}

# resource "kubernetes_ingress_v1" "default_ingress" {

#   metadata {
#     name = "default-ingress"
#     annotations = {
#       "kubernetes.io/ingress.class"                 = "gce"
#       "kubernetes.io/ingress.global-static-ip-name" = local.global_static_ip_name
#       "networking.gke.io/managed-certificates"      = kubectl_manifest.managed_certificate.name
#       "networking.gke.io/v1beta1.FrontendConfig"    = kubectl_manifest.frontend_config.name
#     }
#   }

#   spec {
#     rule {
#       host = var.api_domain
#       http {
#         # Sample Service
#         path {
#           backend {
#             service {
#               name = "sample-service"
#               port {
#                 number = 80
#               }
#             }
#           }
#           path_type = "Prefix"
#           path      = "/sample_service"
#         }
#       }
#     }
#   }

}
