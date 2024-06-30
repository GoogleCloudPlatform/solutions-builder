/**
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

# Terraform Block
terraform {
  required_version = ">= 1.3"
  required_providers {

    google = {
      source  = "hashicorp/google"
      version = ">= 4.50, < 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 4.50, < 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 2.1"
    }
  }

  provider_meta "google" {
    module_name = "blueprints/terraform/terraform-google-lb-http:serverless_negs/v9.0.0"
  }

  provider_meta "google-beta" {
    module_name = "blueprints/terraform/terraform-google-lb-http:serverless_negs/v9.0.0"
  }
}

provider "google" {
  project = var.project_id
}

data "google_client_config" "default" {}

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

output "lb_https_ip_address" {
  value = module.lb-http.external_ip
}
