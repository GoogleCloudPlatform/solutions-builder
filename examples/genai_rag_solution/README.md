# GenAI RAG Solution

> This codebase is generated from https://github.com/GoogleCloudPlatform/solutions-builder

## Prerequisites

| Tool                | Required Version | Installation                                                                                                                                                                                        |
| ------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
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

### Continue to Cloud Infra and foundation steps

Initialize the Cloud infra:

```
gcloud auth login
gcloud auth application-default login
export PROJECT_ID=$(gcloud config get project)
echo PROJECT_ID=$PROJECT_ID
sb set project-id $PROJECT_ID
```

Set up Cloud foundation

```
sb infra apply 1-bootstrap
sb infra apply 2-foundation
sb infra apply 4-genai-service
```

### Upload Samples PDFs to GCS bucket for RAG

Upload sample PDFs to the Cloud Storage bucket.

```
export DOCS_GCS_BUCKET=$PROJECT_ID-sample-docs
gcloud storage cp ./sample_docs/* gs://$DOCS_GCS_BUCKET
```

## Deploy

### Deploy GenAI microservice to Cloud Run.

We use Solutions Builder (as a wrapper of Skaffold) to deploy the instance to Cloud Run.

```
sb deploy -n default -m genai_service
```

### Deploy Frontend (Streamlit) to Cloud Run

```
sb deploy -n default -m frontend
```

## Development

TBD
