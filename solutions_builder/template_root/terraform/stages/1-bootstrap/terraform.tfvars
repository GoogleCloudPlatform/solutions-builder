project_id             = "{{project_id}}"
storage_multiregion    = "US"
region                 = "{{gcp_region}}"
zone                   = "{{gcp_zone}}"
use_jump_host          = "{{use_jump_host}}"
existing_custom_vpc    = "{{create_vpc_network}}"
vpc_network            = "{{vpc_network}}"
vpc_subnetwork         = "{{vpc_subnetwork}}"
ip_cidr_range          = "{{ip_cidr_range}}"
master_ipv4_cidr_block = "{{master_ipv4_cidr_block}}"
secondary_ranges_pods  = {
  range_name    = "secondary-pod-range-01"
  ip_cidr_range = "{{secondary_pod_ip_cidr_range}}"
}
secondary_ranges_services = {
  range_name    = "secondary-service-range-01"
  ip_cidr_range = "{{secondary_service_ip_cidr_range}}"
}
