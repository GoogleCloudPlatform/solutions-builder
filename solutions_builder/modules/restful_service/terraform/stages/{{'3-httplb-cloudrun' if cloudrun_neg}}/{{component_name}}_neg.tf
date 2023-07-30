resource "google_compute_region_network_endpoint_group" "{{component_name}}_neg" {
  name                  = "{{resource_name}}-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = "{{resource_name}}"
  }
}
