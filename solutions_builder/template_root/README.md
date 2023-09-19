# {{project_name}}

> This codebase is generated from https://github.com/GoogleCloudPlatform/solutions-builder

## Prerequisites

| Tool                  | Required Version | Installation |
|-----------------------|------------------|---|
| Python                | &gt;= 3.9        | |
| gcloud CLI            | Latest           | https://cloud.google.com/sdk/docs/install |
| Terraform             | &gt;= v1.3.7     | https://developer.hashicorp.com/terraform/downloads |
| Skaffold              | &gt;= v2.4.0     | https://skaffold.dev/docs/install/ |
| Kustomize             | &gt;= v5.0.0     | https://kubectl.docs.kubernetes.io/installation/kustomize/ |
| solutions-builder CLI | &gt;= v1.13.0    | https://github.com/GoogleCloudPlatform/solutions-builder |

## Setup

### Create a new Google Cloud project

We'd recommend starting from a brand new GCP project. Create a new GCP project at [https://console.cloud.google.com/projectcreate]

### Install Solutions Builder package
```
pip install -U solutions-builder
```

### Set up gcloud CLI
```
export PROJECT_ID=<my-project-id>
gcloud config set project $PROJECT_ID
```

### Check Org policies (Optional)
Make sure that policies are not enforced (`enforce: false` or `NOT_FOUND`). You must be an organization policy administrator to set a constraint.
https://console.cloud.google.com/iam-admin/orgpolicies/compute-requireShieldedVm?project=$PROJECT_ID
https://console.cloud.google.com/iam-admin/orgpolicies/requireOsLogin?project=$PROJECT_ID

### Create jump host for the project (Recommended)
Log in to the jump host
```
sb infra apply 0-jumphost
export JUMP_HOST_ZONE=$(gcloud compute instances list --format="value(zone)")
echo Jump host zone is $JUMP_HOST_ZONE
gcloud compute ssh --zone=$JUMP_HOST_ZONE --tunnel-through-iap jump-host
```

Startup script for the just host (takes about 5-10 min)
```
# Verify that startup script has completed
ls -l /tmp/jumphost_ready

# Look at the output of startup script, in case of errors
sudo journalctl -u google-startup-scripts.service
```

Initialize the Cloud infra:
```
gcloud auth login
gcloud auth application-default login
export PROJECT_ID=$(gcloud config get project)
echo PROJECT_ID=$PROJECT_ID
sb set project-id $PROJECT_ID
sb infra apply 1-bootstrap
```

Set up Cloud foundation
```
sb infra apply 2-foundation
```

## Deploy

### Set up each microservice:

Follow README files of each microservice to setup:
- TBD

### Deploy all microservices (optionally with Ingress) to GKE cluster:
```
sb deploy
```

## Destroy
Turn off deletion protection for the jump host (for `terraform destroy`)
```
gcloud compute instances update jump-host --no-deletion-protection
```

Please refer to [DEVELOPMENT.md](docs/DEVELOPMENT.md) for more details on development and code submission.

## Troubleshoot

Please refer to [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for any Terraform errors

