resource "null_resource" "build_and_deploy_cloudrun" {
  provisioner "local-exec" {
    command = "skaffold run -p cloudrun -m {{component_name}} --default-repo=us-docker.pkg.dev/${var.project_id}/default"
  }
}

resource "google_cloud_run_v2_service" "test_service" {
  depends_on = [
    null_resource.build_container
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
