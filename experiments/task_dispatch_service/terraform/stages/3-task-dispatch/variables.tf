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

# TODO: Add Terraform blocks below.

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

variable "task_pubsub_topic" {
  type        = string
  description = "Pub/Sub topic for Task"
}

variable "message_retention_duration" {
  type        = string
  description = "Pub/Sub message retention duration"
  default     = "86600s"
}

variable "eventarc_trigger_name" {
  type        = string
  description = "EventArc trigger name"
  default     = "trigger-task-pubsub"
}

variable "eventarc_gke_cluster" {
  type        = string
  description = "GKE cluster name used by EventArc"
}

variable "eventarc_gke_namespace" {
  type        = string
  description = "GKE cluster namespace used by EventArc"
  default     = "default"
}

variable "eventarc_gke_path" {
  type        = string
  description = "GKE path used by EventArc"
  default     = "/"
}

variable "eventarc_gke_service" {
  type        = string
  description = "Destination GKE service"
}

variable "eventarc_cloudrun_service" {
  type        = string
  description = "Destination Cloud Run service"
}
