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
  description = "GCP Project ID"

  validation {
    condition     = length(var.project_id) > 0
    error_message = "The project_id value must be an non-empty string."
  }
}

variable "project_number" {
  type        = string
  description = "GCP Project Number"

  validation {
    condition     = length(var.project_number) > 0
    error_message = "The project_number value must be an non-empty string."
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

variable "storage_multiregion" {
  type        = string
  description = "Storage Region or Multiregion"
  validation {
    condition     = length(var.storage_multiregion) > 0
    error_message = "The region value must be an non-empty string."
  }
}

variable "vpc_network" {
  type    = string
  default = "default-vpc"
}

variable "vpc_subnetwork" {
  type    = string
  default = "default-vpc-subnet"
}
