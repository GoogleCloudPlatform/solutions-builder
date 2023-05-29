locals {
  backend_groups = [
    {% for service_name in cloudrun_services.split(",") %}{
      group = format("projects/%s/regions/%s/networkEndpointGroups/%s-neg",
        var.project_id,
        var.region,
        "{{service_name}}")
    },
    {% endfor %}
  ]
}

module "lb-http" {
  depends_on = [
    {% for service_name in cloudrun_services.split(",") %} google_compute_region_network_endpoint_group.{{ service_name.replace("-", "_") }}_neg,
  {% endfor %}]

  source  = "GoogleCloudPlatform/lb-http/google//modules/serverless_negs"
  version = "~> 4.5"

  project = var.project_id
  name    = var.loadbalancer_name
  managed_ssl_certificate_domains = split(",", var.domains)
  ssl                             = true
  https_redirect                  = true

  backends = {
    default = {
      # List your serverless NEGs, VMs, or buckets as backends
      groups = local.backend_groups
      enable_cdn = true

      log_config = {
        enable      = true
        sample_rate = 1.0
      }

      iap_config = {
        enable               = false
        oauth2_client_id     = null
        oauth2_client_secret = null
      }

      description            = null
      custom_request_headers = null
      security_policy        = null
    }
  }
}
