variable "project_id" {
  type        = string
  description = "project ID"
}

variable "region" {
  type        = string
  description = "GCP region"
}

variable "service_name" {
  type        = string
  description = "CloudRun service name"
}

variable "source_dir" {
  type        = string
  description = "Source directory of the CloudRun service"
}

variable "repository_id" {
  type        = string
  description = "Repository ID in Artifact Registry"
}

variable "allow_unauthenticated" {
  type        = bool
  description = "Whether to allow unauthenticated access"

}
