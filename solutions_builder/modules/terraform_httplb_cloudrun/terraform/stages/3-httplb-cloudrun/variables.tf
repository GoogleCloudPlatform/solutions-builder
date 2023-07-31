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

  validation {
    condition     = length(var.region) > 0
    error_message = "The region value must be an non-empty string."
  }
}

variable "loadbalancer_name" {
  type    = string
  default = "http-lb"
}

variable "domains" {
  type        = string
  description = "List of domains attached to the LB, comma-separated."
}

variable "cloudrun_services" {
  type        = string
  description = "List of Cloud Run service names, comma-separated."
}

variable "security_policy" {
  description = "The resource URL for the security policy to associate with the backend service"
  type        = string
  default     = null
}

variable "edge_security_policy" {
  description = "The resource URL for the edge security policy to associate with the backend service"
  type        = string
  default     = null
}

variable "load_balancing_scheme" {
  description = "Load balancing scheme type (EXTERNAL for classic external load balancer, EXTERNAL_MANAGED for Envoy-based load balancer, and INTERNAL_SELF_MANAGED for traffic director)"
  type        = string
  default     = "EXTERNAL"
}
