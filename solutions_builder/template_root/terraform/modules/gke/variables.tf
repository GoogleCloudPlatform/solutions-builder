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
  description = "project ID"
}

variable "cluster_name" {
  type        = string
  description = "GKE cluster name"
}

variable "vpc_network" {
  type        = string
  description = "specify the vpc name"
}

variable "vpc_subnetwork" {
  type        = string
  description = "specify the vpc subnetwork"
}

variable "region" {
  type        = string
  description = "cluster region"
}

variable "node_pool_name" {
  type    = string
  default = "default-pool"
}

variable "enable_private_nodes" {
  type        = bool
  description = "Whether nodes have internal IP addresses only"
  default     = true
}

variable "min_node_count" {
  type        = number
  description = "Minimum number of nodes per zone"
  default     = 1
}

variable "max_node_count" {
  type        = number
  description = "Maximum number of nodes per zone"
  default     = 1
}

variable "machine_type" {
  type        = string
  description = "Node compute engine machine type"
  default     = "n1-standard-8"
}

variable "disk_size_gb" {
  type        = number
  description = "disk_size_gb"
  default     = 1000
}

variable "node_locations" {
  type    = string
  default = ""
}

variable "kubernetes_version" {
  type = string
}

variable "namespace" {
  type        = string
  description = "Kubernetes namespace"
}

variable "service_account_name" {
  type        = string
  description = "Google Service Account name"
}

variable "secondary_ranges_pods" {
  type = object({
    range_name    = string
    ip_cidr_range = string
  })
}

variable "secondary_ranges_services" {
  type = object({
    range_name    = string
    ip_cidr_range = string
  })
}

variable "master_ipv4_cidr_block" {
  type        = string
  description = "The IP range in CIDR notation to use for the hosted master network"
}

variable "source_subnetwork_ip_ranges_to_nat" {
  type        = string
  description = "Defaults to ALL_SUBNETWORKS_ALL_IP_RANGES. How NAT should be configured per Subnetwork. Valid values include: ALL_SUBNETWORKS_ALL_IP_RANGES, ALL_SUBNETWORKS_ALL_PRIMARY_IP_RANGES, LIST_OF_SUBNETWORKS. Changing this forces a new NAT to be created."
  default     = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

variable "gke_service_account_roles" {
  type        = list(string)
  description = "List of GCP IAM roles"
  default = [
    "roles/aiplatform.user",
    "roles/bigquery.admin",
    "roles/datastore.owner",
    "roles/documentai.admin",
    "roles/firebase.admin",
    "roles/iam.serviceAccountUser",
    "roles/logging.admin",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/pubsub.admin",
    "roles/stackdriver.resourceMetadata.writer",
    "roles/secretmanager.admin",
    "roles/storage.admin",
  ]
}
