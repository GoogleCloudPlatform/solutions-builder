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

variable "project_id" {
  type        = string
  description = "GCP Project ID"

  validation {
    condition     = length(var.project_id) > 0
    error_message = "The project_id value must be an non-empty string."
  }
}

variable "region" {
  type        = string
  description = "Default GCP region"
  default     = "us-central1"

  validation {
    condition     = length(var.region) > 0
    error_message = "The region value must be an non-empty string."
  }
}

variable "cluster_name" {
  type    = string
  default = "main-cluster"
}

variable "cluster_external_endpoint" {
  type        = string
  description = "Cluster external endpoint IP address"
}

variable "cluster_ca_certificate" {
  type        = string
  description = "Cluster CA certificate"
}

variable "domains" {
  type        = list(string)
  description = "DNS domain list, excluding protocol. E.g. api.example.com"
  default     = []
}

variable "managed_cert_name" {
  type        = string
  description = "Managed certificate name"
  default     = "managed-cert"
}

variable "frontend_config_name" {
  type        = string
  description = "HTTP Load balancer frontend config name"
  default     = "default-frontend-config"
}
