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

module "vpc" {
  source       = "terraform-google-modules/network/google"
  version      = "~> 5.0"
  project_id   = var.project_id
  network_name = var.vpc_network
  routing_mode = "GLOBAL"

  subnets = [
    {
      subnet_name               = var.serverless_subnet
      subnet_ip                 = "10.10.10.0/28"
      subnet_region             = var.region
      subnet_private_access     = "true"
      subnet_flow_logs          = "true"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
      subnet_flow_logs_sampling = 0.7
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
    },
    {
      subnet_name   = "proxy-only-subnet"
      subnet_ip     = "10.129.0.0/23"
      subnet_region = var.region
      purpose       = "REGIONAL_MANAGED_PROXY"
      role          = "ACTIVE"
    }
  ]

  firewall_rules = [
    {
      name                    = "serverless-to-vpc-connector"
      description             = null
      direction               = "INGRESS"
      priority                = null
      ranges                  = ["107.178.230.64/26", "35.199.224.0/19"]
      source_tags             = null
      source_service_accounts = null
      target_tags             = ["vpc-connector"]
      target_service_accounts = null
      allow = [
        {
          protocol = "tcp"
          ports    = ["667"]
        },
        {
          protocol = "udp"
          ports    = ["665", "666"]
        },
        {
          protocol = "icmp"
          ports    = []
        }
      ]
      deny = []
      log_config = {
        metadata = "EXCLUDE_ALL_METADATA"
      }
    },
    {
      name                    = "vpc-connector-to-serverless"
      description             = null
      direction               = "EGRESS"
      priority                = null
      ranges                  = ["107.178.230.64/26", "35.199.224.0/19"]
      source_tags             = null
      source_service_accounts = null
      target_tags             = ["vpc-connector"]
      target_service_accounts = null
      allow = [
        {
          protocol = "tcp"
          ports    = ["667"]
        },
        {
          protocol = "udp"
          ports    = ["665", "666"]
        },
        {
          protocol = "icmp"
          ports    = []
        }
      ]
      deny = []
      log_config = {
        metadata = "EXCLUDE_ALL_METADATA"
      }
    },
    {
      name                    = "vpc-connector-health-checks"
      description             = null
      direction               = "INGRESS"
      priority                = null
      ranges                  = ["130.211.0.0/22", "35.191.0.0/16", "108.170.220.0/23"]
      source_tags             = null
      source_service_accounts = null
      target_tags             = ["vpc-connector"]
      target_service_accounts = null
      allow = [
        {
          protocol = "tcp"
          ports    = [667]
        }
      ]
      deny = []
      log_config = {
        metadata = "EXCLUDE_ALL_METADATA"
      }
    },
    {
      name                    = "allow-proxy-connection"
      description             = null
      direction               = "INGRESS"
      priority                = null
      ranges                  = ["10.129.0.0/23"]
      source_tags             = null
      source_service_accounts = null
      target_tags             = ["vpc-connector"]
      target_service_accounts = null
      allow = [
        {
          protocol = "tcp"
          ports    = []
        },
      ]
      deny = []
      log_config = {
        metadata = "EXCLUDE_ALL_METADATA"
      }
    }
  ]
}

# resource "google_compute_network" "vpc_network" {
#   name = var.vpc_network
#   auto_create_subnetworks = true
# }

# module "vpc" {
#   source       = "terraform-google-modules/network/google"
#   version      = "~> 4.0"
#   project_id   = var.project_id
#   network_name = var.vpc_network
#   routing_mode = "GLOBAL"
#   auto_create_subnetworks = true
# }

# resource "google_compute_router" "router" {
#   name    = "${var.project_id}-router"
#   region  = var.region
#   network = google_container_cluster.main-cluster.network

#   bgp {
#     asn = 64514
#   }
# }

# resource "google_compute_router_nat" "nat" {
#   name                               = "router-nat"
#   router                             = google_compute_router.router.name
#   region                             = google_compute_router.router.region
#   nat_ip_allocate_option             = "AUTO_ONLY"
#   source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

#   log_config {
#     enable = true
#     filter = "ERRORS_ONLY"
#   }
# }
