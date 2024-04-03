project_id              = "your-project-id" # sb-var:project_id
project_number          = "561278228515" # sb-var:project_number
region                  = "us-central1"     # sb-var:gcp_region
storage_multiregion     = "US"
vpc_network             = "default-vpc"
vpc_subnetwork          = "default-vpc-subset"
ip_cidr_range           = "10.0.0.0/16"
master_ipv4_cidr_block  = "172.16.0.0/28"
firestore_database_name = "(default)"
secondary_ranges_pods = {
  range_name    = "secondary-pod-range-01"
  ip_cidr_range = "10.1.0.0/16"
}
secondary_ranges_services = {
  range_name    = "secondary-service-range-01"
  ip_cidr_range = "10.2.0.0/16"
}
