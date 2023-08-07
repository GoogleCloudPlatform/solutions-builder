variable "project_id" {
  type        = string
  description = "specify the project name"
}

variable "zone" {
  type        = string
  description = "zone for the bastion host"
}

variable "vpc_network_self_link" {
  type        = string
  description = "specify the vpc network self link"
}

variable "vpc_subnetworks_self_link" {
  type        = string
  description = "specify the vpc subnetworks self link"
}

variable "machine_type" {
  type        = string
  description = "Instance type for the Bastion host"
  default     = "n2-standard-4"
}

variable "image" {
  type        = string
  description = "Source image for the Bastion"
  default     = "ubuntu-2004-focal-v20230302"
}

variable "image_family" {
  type        = string
  description = "Source image family for the Bastion"
  default     = "ubuntu-2004"
}

variable "image_project" {
  type        = string
  description = "Project where the source image for the Bastion comes from"
  default     = "ubuntu-os-cloud"
}

variable "disk_size_gb" {
  type        = number
  description = "Boot disk size in GB"
  default     = 200
}

variable "startup_script" {
  type        = string
  description = "startup script to be executed upon provisioning"
  default     = ""
}
