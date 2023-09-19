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

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.65.2"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  services = [
    "compute.googleapis.com",
    "orgpolicy.googleapis.com"
  ]
}

resource "google_project_service" "project-apis" {
  for_each                   = toset(local.services)
  project                    = var.project_id
  service                    = each.value
  disable_dependent_services = true
}

# add timer to avoid errors on new project creation and API enables
resource "time_sleep" "wait_60_seconds" {
  depends_on      = [google_project_service.project-apis]
  create_duration = "60s"
}

resource "google_compute_network" "vpc" {
  depends_on              = [time_sleep.wait_60_seconds]
  project                 = var.project_id
  name                    = "jump-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "jump-vpc-subnet"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.0.0.0/24"
}

resource "google_compute_disk" "default" {
  depends_on = [time_sleep.wait_60_seconds]
  name       = "disk-data"
  type       = "pd-balanced"
  zone       = var.jump_host_zone
  size       = var.disk_size_gb
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = google_compute_network.vpc.self_link

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  # insecure
  source_ranges = ["0.0.0.0/0"]
}

module "cloud-nat" {
  source            = "terraform-google-modules/cloud-nat/google"
  version           = "~> 1.2"
  name              = format("%s-%s-jump-nat", var.project_id, var.region)
  create_router     = true
  router            = format("%s-%s-jump-router", var.project_id, var.region)
  project_id        = var.project_id
  region            = var.region
  network           = google_compute_network.vpc.self_link
  log_config_enable = true
  log_config_filter = "ERRORS_ONLY"
}

data "template_file" "startup_script" {
  template = file("${path.module}/bastion_startup.sh")
}

resource "google_compute_instance" "jump_host" {
  project                   = var.project_id
  zone                      = var.jump_host_zone
  name                      = "jump-host"
  machine_type              = var.machine_type
  deletion_protection       = true
  allow_stopping_for_update = true
  metadata_startup_script   = data.template_file.startup_script.rendered

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-focal-v20230907"
    }
  }

  attached_disk {
    source      = google_compute_disk.default.id
    device_name = google_compute_disk.default.name
  }

  network_interface {
    network    = google_compute_network.vpc.self_link
    subnetwork = google_compute_subnetwork.subnet.self_link
  }

}
