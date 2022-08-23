variable "project_id" {
  type        = string
  description = "project ID"
}

variable "services" {
  type        = list(any)
  description = "List of services to enable"
}