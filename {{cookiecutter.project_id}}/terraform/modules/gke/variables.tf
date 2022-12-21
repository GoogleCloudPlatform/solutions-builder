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

variable "region" {
  type        = string
  description = "cluster region"
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
