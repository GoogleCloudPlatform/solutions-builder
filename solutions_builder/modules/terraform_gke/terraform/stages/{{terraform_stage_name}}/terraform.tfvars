project_id           = "{{project_id}}" # sb-var:project_id
region               = "{{gcp_region}}" # sb-var:gcp_region
kubernetes_version   = "{{kubernetes_version}}"
node_machine_type    = "{{node_machine_type}}"
cluster_name         = "{{cluster_name}}"
private_cluster      = {{private_cluster | lower}}
