project_id              = "{{project_id}}"
project_number          = "{{project_number}}"
region                  = "{{gcp_region}}"
storage_multiregion     = "US"
vpc_network             = "{{vpc_network}}"
vpc_subnetwork          = "{{vpc_subnetwork}}"
ip_cidr_range           = "{{ip_cidr_range}}"
master_ipv4_cidr_block  = "{{master_ipv4_cidr_block}}"
existing_firestore_name = "{{project_id | get_existing_firestore}}"
secondary_ranges_pods = {
  range_name    = "secondary-pod-range-01"
  ip_cidr_range = "{{secondary_pod_ip_cidr_range}}"
}
secondary_ranges_services = {
  range_name    = "secondary-service-range-01"
  ip_cidr_range = "{{secondary_service_ip_cidr_range}}"
}
