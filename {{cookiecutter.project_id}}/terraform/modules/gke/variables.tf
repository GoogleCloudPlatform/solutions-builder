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
  type = number
  description = "Minimum number of nodes per zone"
  default = 1
}

variable "max_node_count" {
  type = number
  description = "Maximum number of nodes per zone"
  default = 1
}

variable "machine_type" {
  type = string
  description = "Node compute engine machine type"
  default = "n1-standard-8"
}

variable "disk_size_gb" {
  type = number
  description = "disk_size_gb"
  default = 1000
}
