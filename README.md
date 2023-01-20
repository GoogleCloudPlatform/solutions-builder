# Google Cloud Solutions Template

> A template to generate a new project with built-in structure and features
> to accelerate your project setup.

## TL;DR

Solutions Template is a boilerplate template for building repeatable
solutions with the best practices in architecture on Google Cloud, including GKE
clusters, CloudRun, Test Automation, CI/CD, as well as development process.

This template provides built-in and ready-to-ship sample features including:
* Container-based microservices, can be deployed to a Kubernetes cluster or CloudRun.
* Simplified deployment using Skaffold and Kustomize
* Google Cloud foundation setup using Terraform
* CI/CD deployment (with Github Actions)
* CloudRun templates

## Roadmap

Please see [Feature Requests in the Github issue list](https://github.com/GoogleCloudPlatform/solutions-template/issues?q=is%3Aopen+is%3Aissue+label%3A%22feature+request%22).

## Prerequisites

### Understanding Google Cloud

We recommend the following resources to get familiar with Google Cloud and microservices.

- What is Microservice Architecture: https://cloud.google.com/learn/what-is-microservices-architecture
- Kubernetes:
  - Learn about the basics of Kubernetes: https://kubernetes.io/docs/concepts/overview/
  - Google Kubernetes Engine (GKE) overview: https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview
  - Skaffold, a command line tool that facilitates continuous development for container based & Kubernetes applications: https://skaffold.dev/docs/
- CloudRun:
  - Serverless container deployment and execution with CloudRun: https://cloud.google.com/run/docs/overview/what-is-cloud-run

### Tool requirements:

| Tool  | Required Version  | Documentation site |
|---|---|---|
| gcloud CLI | Latest     | https://cloud.google.com/sdk/docs/install |
| Terraform  | >= v1.3.7  | https://developer.hashicorp.com/terraform/downloads |
| Skaffold   | >= v2.0.4  | https://skaffold.dev/ |
| Kustomize  | >= v4.3.1  | https://kustomize.io/ |
| Cookiecutter  | >=2.1.1  | https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter |

### Apple M1 Chip Support for Terraform (Optional)

If you are running commands on an Apple M1 chip Macbook, make sure run the following to add M1 support for Terraform:
```
brew install kreuzwerker/taps/m1-terraform-provider-helper
m1-terraform-provider-helper activate
m1-terraform-provider-helper install hashicorp/template -v v2.2.0
```

## Getting Started - Creating Solution Skeleton

### (Optional) Create a new Google Cloud project:

> It is recommeneded to start with a brand new Google Cloud project to have a clean start.

Run the following to create a new Google Cloud project, or you can log in to Google Cloud Console to [create a new project](https://console.cloud.google.com/projectcreate).
```
export PROJECT_ID=<my-gcp-project-id>
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID
```

### Install Cookiecutter ([Github](https://github.com/cookiecutter/cookiecutter)):
- For Google CloudShell or Linux/Ubuntu:
  ```
  python3 -m pip install --user cookiecutter
  ```
- For MacOS:
  ```
  brew install cookiecutter
  ```
- For Windows, refer this [installation guide](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter)

### Create skeleton code in a new folder with Cookiecutter

Run the following to generate skeleton code in a new folder (project id will be chosen later):
```
cookiecutter https://github.com/GoogleCloudPlatform/solutions-template.git
```

Provide the required variables to Cookiecutter prompt, e.g.:
```
project_id: my-gcp-project-id
project_name [My Awesome Project]:
project_short_description [My Awesome Project]:
project_slug [my_project]:
Google Cloud_region [us-central1]:
version [0.1.0]:
admin_email [admin@example.com]:
```
- The `project_id` is your Google Cloud project ID.
- You may leave variables as blank if you'd like to use the default value (except projdct_id).
- Notes: If you run into any issues with `cookiecutter`, please add `--verbose` at
the end of the command to show detailed errors.

Once `cookiecutter` completes, you will see the folder `<project_id>` created in
the path where you ran `cookiecutter` command.

### Inside the newly created folder

You will see the file structure like below:
```
<project_id>/
│   README.md
|   DEVELOPMENT.md
│   skaffold.yaml
│
└───microservices/
│   └───sample_service/
│       └───kustomize/
│       └───src/
│       │   Dockerfile
│       │   requirements.txt
│       │   skaffold.yaml
│       │   ...
│
└───common/
│   └───src/
│   │   Dockerfile
│   │   requirements.txt
│   │   skaffold.yaml
│   │   ...
│
└───.github/

```
### File structure details

- **README.md** - This contains steps and deployment details to get started with the generated code.
- **DEVELOPMENT.md** - This contains guidance for developers including development best practices, code submission flow, and troubleshootings.
- **skaffold.yaml** - This is the master Skaffold YAML file that defines how everything is built and deployed, depending on different profiles.
- **microservices** - The main directory for all microservices, can be broken down into individual folder for each microservie, e.g. `sample_service`.
  - [**microservice subfolder**] - Each microservice folder is a Docker container with [Skaffold](https://skaffold.dev/) + [Kustomize](https://kustomize.io/) to build images in different environments.
- **common** - The common image contains shared data models and util libraries used by all other microservices.


## Getting Started - Setting up Google Cloud project

Once the solution skeleton code generated in **your-project-folder** folder, the next step is to set up the Google Cloud project.
You will also find the same steps in the `README.md` inside **your-project-folder**.

This guide will detail how to set up your new solutions template project. See the [development guide](./DEVELOPMENT.md) for how to contribute to the project.

### Set up working environment:
```
# Set up environmental variables
export PROJECT_ID=<my-gcp-project-id>
export ADMIN_EMAIL=<my-email>
export REGION=us-central1
export API_DOMAIN=localhost

cd $PROJECT_ID
export BASE_DIR=$(pwd)

# Login to Google Cloud (if not on Cloud Shell)
gcloud auth application-default login
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID
```

### Updating GCP Organizational policies

Run the following commands to update Organization policies:
```
export ORGANIZATION_ID="$(gcloud organizations list --format="value(name)" | head -n 1)"
gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
```

Or, change the following Organization policy constraints in [GCP Console](https://console.cloud.google.com/iam-admin/orgpolicies)
- constraints/compute.requireOsLogin - `Enforced Off`
- constraints/compute.vmExternalIpAccess - `Allow All`

###  Setting up GCP foundation - Terraform

Set up Terraform environment variables and GCS bucket for state file.
If the new project is just created recently, you may need to wait for 1-2 minutes
before running the Terraform command.

```
export TF_VAR_project_id=$PROJECT_ID
export TF_VAR_api_domain=$API_DOMAIN
export TF_VAR_web_app_domain=$API_DOMAIN
export TF_VAR_admin_email=$ADMIN_EMAIL
export TF_BUCKET_NAME="${PROJECT_ID}-tfstate"
export TF_BUCKET_LOCATION="us"

# Grant Storage admin to the current user IAM.
export CURRENT_USER=$(gcloud config list account --format "value(core.account)")
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$CURRENT_USER" --role='roles/storage.admin'

# Create Terraform Statefile in GCS bucket.
bash setup/setup_terraform.sh
```

> NOTE: If you run into errors with unlinked billing account. Please go to https://console.cloud.google.com/billing/linkedaccount to set up the billing account of the current Google Cloud project.

Init and run Terraform apply

```
# Init Terraform
cd terraform/environments/dev
terraform init -backend-config=bucket=$TF_BUCKET_NAME

# Enabling GCP services first.
terraform apply -target=module.project_services -target=module.service_accounts -auto-approve

# Initializing Firebase (Only need this for the first time.)
# NOTE: the Firebase can only be initialized once (via App Engine).
terraform apply -target=module.firebase -var="firebase_init=true" -auto-approve

# Run the rest of Terraform
terraform apply -auto-approve
```

### Deploying Kubernetes Microservices to GKE

> You can skip this section if you plan to deploy microservices with CloudRun.

Install required packages:

- For Google CloudShell or Linux/Ubuntu:
  ```
  export SKAFFOLD_VERSION=v2.0.4
  curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/$SKAFFOLD_VERSION/skaffold-linux-amd64 && \
  sudo install skaffold /usr/local/bin/
  ```
- For MacOS:
  ```
  brew install --cask skaffold kustomize google-cloud-sdk
  ```
- For Windows:
  ```
  choco install -y skaffold kustomize gcloudsdk
  ```

> Make sure to use __skaffold 2.0.4__ or later for development.

Build all microservices (including web app) and deploy to the cluster:
```
cd $BASE_DIR
export CLUSTER_NAME=main-cluster
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION --project $PROJECT_ID
skaffold run -p prod --default-repo=gcr.io/$PROJECT_ID
```

Test with API endpoint:
```
export API_DOMAIN=$(kubectl describe ingress | grep Address | awk '{print $2}')
export URL="http://${API_DOMAIN}/sample_service/docs"
echo "Open this URL in a browser: ${URL}"
```

### (Optional) Deploying Microservices to CloudRun

Open `terraform/environments/dev/main.tf`, and uncomment the CloudRun section like below:

```
# [Optional] Deploy sample-service to CloudRun
# Uncomment below to enable deploying microservices with CloudRun.
module "cloudrun-sample" {
  depends_on = [module.project_services, module.vpc_network]

  source                = "../../modules/cloudrun"
  project_id            = var.project_id
  region                = var.region
  source_dir            = "../../../microservices/sample_service"
  service_name          = "cloudrun-sample"
  repository_id         = "cloudrun"
  allow_unauthenticated = true
}
```

## FAQ
- Who are the target audience/users for this Solutions template?
  - A: Any engineering team to start a new solution development project.
- Can I choose to deploy microservice just to CloudRun?
  - A: Yes, please follow steps in the README.md in **your-project-folder** generated from cookiecutter.

## Troubleshoots

- I use a Apple M1 Mac and got errors like below when I ran `terraform init`:
  ```
  │ Error: Incompatible provider version
  │
  │ Provider registry.terraform.io/hashicorp/template v2.2.0 does not have a package available for your current platform,
  │ darwin_arm64.
  │
  │ Provider releases are separate from Terraform CLI releases, so not all providers are available for all platforms. Other
  │ versions of this provider may have different platforms supported.
  ```
  - A: Run the following to add support of M1 chip ([reference](https://kreuzwerker.de/en/post/use-m1-terraform-provider-helper-to-compile-terraform-providers-for-mac-m1))
    ```
    brew install kreuzwerker/taps/m1-terraform-provider-helper
    m1-terraform-provider-helper activate
    m1-terraform-provider-helper install hashicorp/template -v v2.2.0
    ```