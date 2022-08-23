variable "project_id" {
  type        = string
  description = "project ID"
}

variable "region" {
  type        = string
  description = "GCP region"
}

variable "cert_issuer_email" {
  type        = string
  description = "email of the cert issuer"
}

variable "domain" {
  type        = string
  description = "Ingress base domain, excluding protocol. E.g. api.example.com"
}

variable "cors_allow_origin" {
  type        = string
  description = "CORS allow origins, comma-seperated."
}
