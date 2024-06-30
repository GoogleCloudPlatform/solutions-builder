# {{project_name}}

> This codebase is generated from https://github.com/GoogleCloudPlatform/solutions-builder

## Overview

### Context & Background

TODO: Fill in context & background

### Objectives & Scope

TODO: Fill in objectives & scope

### Project Timeline

TODO: Fill in Project Timeline

## Setup

### Prerequisite

| Tool              | Required Version | Installation                                             |
| ----------------- | ---------------- | -------------------------------------------------------- |
| Python            | &gt;= 3.11       |                                                          |
| gcloud CLI        | Latest           | https://cloud.google.com/sdk/docs/install                |
| Terraform         | &gt;= v1.3.7     | https://developer.hashicorp.com/terraform/downloads      |
| Skaffold          | &gt;= v2.4.0     | https://skaffold.dev/docs/install/#standalone-binary     |
| solutions-builder | latest           | https://github.com/GoogleCloudPlatform/solutions-builder |

[Optional] For deploying to a GKE cluster, please install the following:

| Tool      | Required Version | Installation                                               |
| --------- | ---------------- | ---------------------------------------------------------- |
| Kustomize | &gt;= v5.0.0     | https://kubectl.docs.kubernetes.io/installation/kustomize/ |

### Set up a GCP project

To start from a brand new GCP project, create a new GCP project and set the billing account:

```
export PROJECT_ID=my-project-id
export BILLING_ACCOUNT=$(gcloud alpha billing accounts list --format='value(ACCOUNT_ID)')
gcloud projects create $PROJECT_ID
gcloud projects set-billing-account $PROJECT_ID $BILLING_ACCOUNT
gcloud config set project $PROJECT_ID

```

### Install Solutions Builder CLI

With `pip`:

```
pip install solutions-builder
```

With `pipx`:

```
pip install --user pipx && pipx install solutions-builder
```

### Initialize the Cloud infrastructure (Terraform)

```
sb terraform apply --all
```

- This will run `terraform init` commands in all stages folder.
-

## Deploy

### Deploy all microservices

Deploy all services to Cloud Run

```
sb deploy -m cloudrun
```

- All services are defined in the root `skaffold.yaml`.

Or, deploy all services to a GKE cluster:

```
sb deploy -m gke
```

### Other deployment options

For other deployment and scenarios, please see https://github.com/GoogleCloudPlatform/solutions-builder/blob/main/docs/CLI_USAGE.md

## Design

TODO: Fill in your design here.

## Development

TODO: Fill in your development details here.
