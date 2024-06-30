resource "null_resource" "{{component_name}}_build_container" {
  provisioner "local-exec" {
    command = "cd ../../../ && skaffold build -p cloudrun -m {{component_name}} --default-repo=us-docker.pkg.dev/${var.project_id}/default"
  }
}

resource "google_cloud_run_v2_service" "{{component_name}}" {
  depends_on = [
    null_resource.{{component_name}}_build_container
  ]
  name     = "{{resource_name}}"
  project  = var.project_id
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/${var.project_id}/default/{{resource_name}}:latest"
    }
  }
}

resource "google_compute_region_network_endpoint_group" "{{component_name}}_neg" {
  name                  = "{{resource_name}}-neg"
  network_endpoint_type = "SERVERLESS"
  project               = var.project_id
  region                = var.region
  cloud_run {
    service = "{{resource_name}}"
  }
}
