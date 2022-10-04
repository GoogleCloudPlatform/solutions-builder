module "vpc" {
  source       = "terraform-google-modules/network/google"
  version      = "~> 4.0"
  project_id   = var.project_id
  network_name = var.vpc_network
  routing_mode = "GLOBAL"

  subnets = [
    {
      subnet_name               = "vpc-01-subnet-01"
      subnet_ip                 = "10.0.0.0/16"
      subnet_region             = "us-central1"
      subnet_flow_logs          = "true"
      subnet_flow_logs_interval = "INTERVAL_10_MIN"
      subnet_flow_logs_sampling = 0.7
      subnet_flow_logs_metadata = "INCLUDE_ALL_METADATA"
    }
  ]

  secondary_ranges = {
    vpc-01-subnet-01 = [
      {
        range_name    = "secondary-pod-range-01"
        ip_cidr_range = "10.1.0.0/16"
      },
      {
        range_name    = "secondary-service-range-01"
        ip_cidr_range = "10.2.0.0/16"
      },
    ]
  }
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

# module "cloud-nat" {
#   source            = "terraform-google-modules/cloud-nat/google"
#   version           = "~> 1.2"
#   name              = format("%s-%s-nat", var.project_id, var.region)
#   create_router     = true
#   router            = format("%s-%s-router", var.project_id, var.region)
#   project_id        = var.project_id
#   region            = var.region
#   network           = module.vpc.network_id
#   log_config_enable = true
#   log_config_filter = "ERRORS_ONLY"
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
