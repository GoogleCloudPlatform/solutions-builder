ip_cidr_range = "10.0.0.0/16"
master_ipv4_cidr_block = "172.16.0.0/28"
secondary_ranges_pods = {
  "ip_cidr_range" = "10.1.0.0/16"
  "range_name" = "secondary-pod-range-01"
}
secondary_ranges_services = {
  "ip_cidr_range" = "10.2.0.0/16"
  "range_name" = "secondary-service-range-01"
}
vpc_network = "default-vpc"
vpc_subnetwork = "default-vpc-subset"
