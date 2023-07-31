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
  description = "specify the project name"
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
  description = "GCP region"
}

variable "subnet_ip" {
  type        = string
  description = "10.0.0.0/16"
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
