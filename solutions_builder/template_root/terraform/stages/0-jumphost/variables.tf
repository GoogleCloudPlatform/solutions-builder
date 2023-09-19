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

variable "jump_host_zone" {
  type        = string
  description = "GCP Zone for the jump host"
}

variable "machine_type" {
  type        = string
  description = "Instance type for the Bastion host"
  default     = "n2-standard-2"
}

variable "disk_size_gb" {
  type        = number
  description = "Boot disk size in GB"
  default     = 200
}
