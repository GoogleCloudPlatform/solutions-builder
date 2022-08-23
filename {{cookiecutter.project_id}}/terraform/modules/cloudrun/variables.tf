variable "project_id" {
  type        = string
  description = "project ID"
}

variable "region" {
  type        = string
  description = "GCP region"
}

variable "services" {
  type        = list(any)
  description = "List of CloudRun services"
}
