# {{project_name}}

> This codebase is generated from https://github.com/GoogleCloudPlatform/solutions-builder

## Prerequisites

| Tool                | Required Version | Installation                                                                                                                                                                                        |
|---------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `python`            | `>= 3.9`         | [Mac](https://www.python.org/ftp/python/3.9.18/python-3.9.18-macos11.pkg) • [Windows](https://www.python.org/downloads/release/python-3918/) • [Linux](https://docs.python.org/3.9/using/unix.html) |
| `gcloud` CLI        | `Latest`         | https://cloud.google.com/sdk/docs/install                                                                                                                                                           |
| `terraform`         | `>= v1.3.7`      | https://developer.hashicorp.com/terraform/downloads                                                                                                                                                 |
| `solutions-builder` | `>= v1.17.19`    | https://pypi.org/project/solutions-builder/                                                                                                                                                         |
| `skaffold`          | `>= v2.4.0`      | https://skaffold.dev/docs/install/                                                                                                                                                                  |
| `kustomize`         | `>= v5.0.0`      | https://kubectl.docs.kubernetes.io/installation/kustomize/                                                                                                                                          |

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
```
gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --project="${PROJECT_ID}"
gcloud resource-manager org-policies disable-enforce constraints/compute.requireShieldedVm --project="${PROJECT_ID}"
gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --project="${PROJECT_ID}"
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --project="${PROJECT_ID}"
```
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

Note: For a fresh start, here are the steps to delete/destroy jump host and corresponding resources from project. However, this not clean up any resources that were deployed from the jump host
```
gcloud compute instances update jump-host --no-deletion-protection --project="${PROJECT_ID}"
sb infra destroy 0-jumphost
```
### Continue to Cloud Infra and foundation steps
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

## Development

Please refer to [DEVELOPMENT.md](docs/DEVELOPMENT.md) for more details on development and code submission.

## Troubleshoot

Please refer to [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for any Terraform errors

