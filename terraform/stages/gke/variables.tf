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

variable "env" {
  type    = string
  default = "dev"
}

variable "project_id" {
  type        = string
  description = "GCP Project ID"

  validation {
    condition     = length(var.project_id) > 0
    error_message = "The project_id value must be an non-empty string."
  }
}

variable "vpc_network" {
  type    = string
  default = "gke-vpc"
}

variable "vpc_subnetwork" {
  type    = string
  default = "gke-vpc-subnet"
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

variable "ip_cidr_range" {
  type    = string
  default = "10.0.0.0/16"
}

variable "secondary_ranges_pods" {
  type = object({
    range_name    = string
    ip_cidr_range = string
  })
  default = {
    range_name    = "secondary-pod-range-01"
    ip_cidr_range = "10.1.0.0/16"
  }
}

variable "secondary_ranges_services" {
  type = object({
    range_name    = string
    ip_cidr_range = string
  })
  default = {
    range_name    = "secondary-service-range-01"
    ip_cidr_range = "10.2.0.0/16"
  }
}

variable "master_ipv4_cidr_block" {
  type        = string
  description = "The IP range in CIDR notation to use for the hosted master network"
  default     = "172.16.0.0/28"
}

variable "firestore_region" {
  type        = string
  description = "Firestore Region"
  default     = "us-central"
}

variable "bq_dataset_location" {
  type        = string
  description = "BigQuery Dataset location"
  default     = "US"
}

variable "storage_multiregion" {
  type    = string
  default = "us"
}

variable "admin_email" {
  type = string
  # TODO: replace with your own email
  default = "admin@google.com"
}

variable "api_domain" {
  type        = string
  description = "API endpoint domain, excluding protocol"
  default     = "localhost"
}

variable "web_app_domain" {
  type        = string
  description = "Web app domain, excluding protocol"
  default     = "localhost:8080"
}
