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

# In this ingress module, it uses Nginx as the ingress controller to serve
# as a L4 load balancer. Installing nginx requires helm to simply the steps.
#

# Terraform Block
terraform {
  required_version = ">= 0.13"
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }
  }
}

# Create a namespace for ingress object and ingress controller.
resource "kubernetes_namespace" "ingress_nginx" {
  metadata {
    name = "ingress-nginx"
  }
}

# Create a global static IP address for ingress controller.
# Once created, check the IP address here: https://console.cloud.google.com/networking/addresses/list
resource "google_compute_global_address" "ingress_ip_address" {
  name = "ingress-static-ip"
}

module "cert_manager" {
  source                                 = "terraform-iaac/cert-manager/kubernetes"
  cluster_issuer_email                   = var.cert_issuer_email
  cluster_issuer_name                    = "letsencrypt"
  cluster_issuer_private_key_secret_name = "cert-manager-private-key"
  # Letsencrypt has rate limits on prod, so we'll use staging server her.
  cluster_issuer_server = "https://acme-staging-v02.api.letsencrypt.org/directory"
  # Requires additional set to helm. See https://cert-manager.io/docs/installation/compatibility/#gke
  # and https://github.com/cert-manager/cert-manager/issues/3717#issuecomment-972088152
  additional_set = [{
    name  = "global.leaderElection.namespace"
    value = "ingress-nginx"
  }]

  # Workaround to let nginx controller to read secret from cert-manager.
  # See https://github.com/kubernetes/ingress-nginx/issues/2170
  namespace_name   = "ingress-nginx"
  create_namespace = false
}

# Install nginx as the ingress controller. It uses [helm](https://helm.sh/)
# to install nginx controller.
module "nginx-controller" {
  depends_on = [
    # module.cert_manager, # Wait for cert manager to have the secret "cert-manager-private-key" ready.
    resource.kubernetes_namespace.ingress_nginx
  ]

  source     = "terraform-iaac/nginx-controller/helm"
  version    = "2.0.2"
  namespace  = "ingress-nginx"
  ip_address = google_compute_global_address.ingress_ip_address.address
}

# Setting up ingress object as the set of rules of routing. It uses
# "kubernetes_ingress_v1" instead of "kubernetes_ingress"
resource "kubernetes_ingress_v1" "default_ingress" {
  depends_on = [
    google_compute_global_address.ingress_ip_address
  ]

  metadata {
    name = "default-ingress"
    annotations = {
      "kubernetes.io/ingress.global-static-ip-name"        = google_compute_global_address.ingress_ip_address.name
      "kubernetes.io/ingress.class"                        = "nginx"
      "cert-manager.io/cluster-issuer"                     = module.cert_manager.cluster_issuer_name
      "nginx.ingress.kubernetes.io/enable-cors"            = "true"
      "nginx.ingress.kubernetes.io/cors-allow-methods"     = "PUT,GET,POST,DELETE,OPTIONS"
      "nginx.ingress.kubernetes.io/cors-allow-origin"      = var.cors_allow_origin
      "nginx.ingress.kubernetes.io/cors-allow-credentials" = "true"
      "nginx.ingress.kubernetes.io/proxy-read-timeout"     = "3600"
    }
  }

  spec {
    rule {
      http {
        # Sample Service
        path {
          backend {
            service {
              name = "sample-service"
              port {
                number = 80
              }
            }
          }
          path_type = "Prefix"
          path      = "/sample_service"
        }
      }
    }

    tls {
      secret_name = "cert-manager-private-key"
    }
  }
}
