locals {
  {% set service_names = cloudrun_services.split(",") %}
  service_names = [{% for service_name in service_names %}
    {% if service_name != "" %}"{{service_name}}",{% endif %}{% endfor %}
  ]
}

module "compute_backend_services" {
  depends_on = [{% for service_name in cloudrun_services.split(",") %}
    {% if service_name != "" %}google_compute_region_network_endpoint_group.{{ service_name.replace("-", "_") }}_neg,{% endif %}{% endfor %}
  ]
  source   = "../../modules/compute_backend"
  name     = var.loadbalancer_name
  project  = var.project_id
  backends = { {% for service_name in cloudrun_services.split(",") %}
    {% if service_name != "" %}{{service_name}} = {
      # List your serverless NEGs, VMs, or buckets as backends
      groups = [
        {
          group = format("projects/%s/regions/%s/networkEndpointGroups/%s-neg",
            var.project_id,
            var.region,
            "{{service_name}}")
        }
      ]

      # TODO: Fix cdn_policy
      enable_cdn = false

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
    {% endif %}{% endfor %}
  }

}

resource "google_compute_url_map" "httplb_urlmap" {
  depends_on = [
    module.compute_backend_services
  ]

  name        = "${var.loadbalancer_name}-urlmap"
  description = "URL map for CloudRun services"
  default_service = "${var.loadbalancer_name}-backend-{{service_names[0]}}"

  host_rule {
    hosts        = [split(",", var.domains)[0]]
    path_matcher = "allpaths"
  }

  path_matcher {
    name            = "allpaths"

    # Uncomment this and change to your default backend service name.
    default_service = "${var.loadbalancer_name}-backend-{{service_names[0]}}"

    {% for service_name in cloudrun_services.split(",") %}{% if service_name != "" %}path_rule {
      paths   = [
        "/{{service_name}}",
        "/{{service_name}}/*",
      ]
      service = "${var.loadbalancer_name}-backend-{{service_name}}"
    }
    {% endif %}{% endfor %}
  }
}

module "lb-http" {
  depends_on = [
    google_compute_url_map.httplb_urlmap,
  ]

  source  = "GoogleCloudPlatform/lb-http/google//modules/serverless_negs"
  version = "~> 9.0"

  project = var.project_id
  name    = var.loadbalancer_name
  managed_ssl_certificate_domains = split(",", var.domains)
  ssl            = true
  https_redirect = true
  create_url_map = false
  url_map        = "${var.loadbalancer_name}-urlmap"

  # Create LB without backends to avoid cicular dep.
  backends = {}
}
