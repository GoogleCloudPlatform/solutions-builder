# Terraform Block
terraform {
  required_version = ">= 0.13"
  required_providers {
    kubectl = {
      source = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.5.1"
    }
  }
}

module "cert_manager" {
  source = "terraform-iaac/cert-manager/kubernetes"

  cluster_issuer_email                   = var.cert_issuer_email
  cluster_issuer_name                    = "letsencrypt"
  cluster_issuer_private_key_secret_name = "cert-manager-private-key"
}

resource "kubernetes_namespace" "ingress_nginx" {
  metadata {
    name = "ingress-nginx"
  }
}

resource "google_compute_address" "ingress_ip_address" {
  name = "nginx-controller"
}

module "nginx-controller" {
  source    = "terraform-iaac/nginx-controller/helm"
  version   = "2.0.2"
  namespace = "ingress-nginx"

  ip_address = google_compute_address.ingress_ip_address.address

  # TODO: does this require cert_manager up and running or can they be completed in parallel
  depends_on = [
    module.cert_manager, resource.kubernetes_namespace.ingress_nginx
  ]
}

resource "kubernetes_ingress_v1" "default_ingress" {
  metadata {
    name = "default-ingress"
    annotations = {
      "kubernetes.io/ingress.class" = "nginx"
      "cert-manager.io/cluster-issuer" = "letsencrypt"
      "nginx.ingress.kubernetes.io/enable-cors" = "true"
      "nginx.ingress.kubernetes.io/cors-allow-methods" = "PUT,GET,POST,DELETE,OPTIONS"
      "nginx.ingress.kubernetes.io/cors-allow-origin" = var.cors_allow_origin
      "nginx.ingress.kubernetes.io/cors-allow-credentials" = "true"
      "nginx.ingress.kubernetes.io/proxy-read-timeout" = "3600"
    }
  }

  spec {
    rule {
      http {
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
          path = "/sample_service"
        }
      }
    }

    tls {
      secret_name = "tls-secret"
    }
  }
}

# resource "kubectl_manifest" "ingress" {
#   yaml_body = <<YAML
# kind: Ingress
# apiVersion: networking.k8s.io/v1
# metadata:
#   name: default-nginx-ingress
#   annotations:
#     kubernetes.io/ingress.class: "nginx"
#     cert-manager.io/cluster-issuer: "letsencrypt"
#     nginx.ingress.kubernetes.io/enable-cors: "true"
#     nginx.ingress.kubernetes.io/cors-allow-methods: "PUT, GET, POST, OPTIONS, DELETE"
#     nginx.ingress.kubernetes.io/cors-allow-origin: "${var.cors_allow_origin}"
#     nginx.ingress.kubernetes.io/cors-allow-credentials: "true"
#     nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
# spec:
#   tls:
#     - hosts:
#       - ${var.domain}
#       secretName: ${var.domain}-ssl-cert
#   rules:
#   - host: ${var.domain}
#     http:
#       paths:
#       - pathType: Prefix
#         path: /sample_service
#         backend:
#           service:
#             name: sample-service
#             port:
#               number: 80

# YAML

#   depends_on = [
#     module.nginx-controller
#   ]
# }
