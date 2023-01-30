# Google Cloud Solutions Template

> A template to generate a new project with built-in structure and features
> to accelerate your project setup.

## TL;DR

Solutions Template is a boilerplate template for building repeatable
solutions with the best practices in architecture on Google Cloud, including GKE
clusters, Cloud Run, Test Automation, CI/CD, as well as development process.

This template provides built-in and ready-to-ship sample features including:
* Container-based microservices, can be deployed to a Kubernetes cluster or Cloud Run.
* Simplified deployment using Skaffold and Kustomize
* Google Cloud foundation setup using Terraform
* CI/CD deployment (with Github Actions)
* Cloud Run templates

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
- Cloud Run:
  - Serverless container deployment and execution with Cloud Run: https://cloud.google.com/run/docs/overview/what-is-cloud-run

### Tool requirements:

| Tool  | Required Version  | Documentation site |
|---|---|---|
| gcloud CLI          | Latest     | https://cloud.google.com/sdk/docs/install |
| Terraform           | >= v1.3.7  | https://developer.hashicorp.com/terraform/downloads |
| Skaffold (for GKE)  | >= v2.0.4  | https://skaffold.dev/ |
| Kustomize (for GKE) | >= v4.3.1  | https://kustomize.io/ |
| Cookiecutter        | >=2.1.1    | https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter |

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

### Required packages for deploying to GKE cluster:
> You can skip this section if you choose to deploy microservices to Cloud Run only.

Install **skaffold (2.0.4 or later)** and kustomize:

- For Google CloudShell or Linux/Ubuntu:
  ```
  export SKAFFOLD_VERSION=v2.0.4
  curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/$SKAFFOLD_VERSION/skaffold-linux-amd64 && \
  sudo install skaffold /usr/local/bin/
  ```
- For MacOS:
  ```
  brew install skaffold kustomize
  ```
- For Windows:
  ```
  choco install -y skaffold kustomize gcloudsdk
  ```

### Apple M1 Chip Support for Terraform (Optional)

If you are running commands on an Apple M1 chip Macbook, make sure run the following to add M1 support for Terraform:
```
brew install kreuzwerker/taps/m1-terraform-provider-helper
m1-terraform-provider-helper activate
m1-terraform-provider-helper install hashicorp/template -v v2.2.0
```

## Getting Started - Creating Solution Skeleton

### Create a new Google Cloud project (Optional):

> It is recommeneded to start with a brand new Google Cloud project to have a clean start.

Run the following to create a new Google Cloud project, or you can log in to Google Cloud Console to [create a new project](https://console.cloud.google.com/projectcreate).
```
export PROJECT_ID=<my-gcp-project-id>
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID
```

### Create skeleton code in a new folder with Cookiecutter

Run the following to generate skeleton code in a new folder:
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
- **DEVELOPMENT.md** - This contains guidance for developers including development best practices, code submission flow, and other guidances.
- **skaffold.yaml** - This is the master Skaffold YAML file that defines how everything is built and deployed, depending on different profiles.
- **microservices** - The main directory for all microservices, can be broken down into individual folder for each microservie, e.g. `sample_service`.
  - [**microservice subfolder**] - Each microservice folder is a Docker container with [Skaffold](https://skaffold.dev/) + [Kustomize](https://kustomize.io/) to build images in different environments.
- **common** - The common image contains shared data models and util libraries used by all other microservices.

Once the solution skeleton code generated in **your-project-folder** folder, you have two options to set up your Google Cloud project:
- Setting up with setup_all script.
- Or, Setting up with Manual Steps.

## Getting Started - Setting up with setup_all script (Recommended)

Please make sure you are in the generated folder: **your-project-folder**

```
# Set up environmental variables
export PROJECT_ID=<my-gcp-project-id>
export ADMIN_EMAIL=<my-email>
export REGION=us-central1
export API_DOMAIN=localhost
export BASE_DIR=$(pwd)
```

Log in to Google Cloud.
```
# Login to Google Cloud (if not on Cloud Shell)
gcloud auth login
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID
```

Run setup_all.sh to run all steps:
```
# Choose the microservice deployment option: "gke" or "cloudrun"
export MICROSERVICE_DEPLOYMENT_OPTION="gke"

# Run all setup steps.
sh setup/setup_all.sh
```

It will then run the following steps:
- Updating GCP Organizational policies and required IAM roles.
- Run terraform to set up foundation and GKE cluster.
- Build and deploy microservices to GKE cluster.
- Test API endpoints (pytest).

## Getting Started - Setting up with Manual Steps

> The section covers manual setup steps, as same as in the `README.md` generated inside **your-project-folder**.

### Set up working environment:

Please make sure you are in the generated folder: **your-project-folder**

```
# Set up environmental variables
export PROJECT_ID=<my-gcp-project-id>
export ADMIN_EMAIL=<my-email>
export REGION=us-central1
export API_DOMAIN=localhost
export BASE_DIR=$(pwd)
```

Log in to Google Cloud.
```
# Login to Google Cloud (if not on Cloud Shell)
gcloud auth login
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID
```

### Updating GCP Organizational policies

Run the following commands to update Organization policies:
```
export ORGANIZATION_ID=$(gcloud organizations list --format="value(name)" | head -n 1)
gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
```

Or, go to [GCP Console](https://console.cloud.google.com/iam-admin/orgpolicies) and change the following Organization policy constraints:
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
export CURRENT_USER=$(gcloud config list account --format "value(core.account)" | head -n 1)
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$CURRENT_USER" --role='roles/storage.admin'

# (Optional) Link billing account to the current project.
export BILLING_ACCOUNT=$(gcloud beta billing accounts list --format "value(name)" | head -n 1)
gcloud beta billing projects link $PROJECT_ID --billing-account $BILLING_ACCOUNT
```

Create Terraform Statefile in GCS bucket.
```
bash setup/setup_terraform.sh
```

> NOTE: If you run into errors with unlinked billing account. Please go to https://console.cloud.google.com/billing/linkedaccount to set up the billing account of the current Google Cloud project.

Init and run Terraform apply. This will create the follow resources:
- A default VPC network.
- Initialize Firestore project.
- A default service account for deployment.

```
# Init Terraform
cd $BASE_DIR/terraform/stages/foundation
terraform init -backend-config=bucket=$TF_BUCKET_NAME

# Enabling GCP services first.
terraform apply -target=module.project_services -target=module.service_accounts -auto-approve

# Initializing Firebase (Only for the first time.)
# NOTE: the Firebase can only be initialized once (via App Engine).
terraform apply -target=module.firebase -var="firebase_init=true" -auto-approve

# Run the rest of Terraform
terraform apply -auto-approve
```

### Deploying Microservices to GKE (Optional)

Init GKE cluster (via Terraform). This will create the follow resources:
- A GKE cluster
- Service account for GKE

```
cd $BASE_DIR/terraform/stages/gke
terraform init -backend-config=bucket=$TF_BUCKET_NAME
terraform apply -auto-approve
```

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
- When opening up the URL, you will see the Swagger frontend page with available API endpoint description.

Run API tests (Optional):
```
# Run API tests
python e2e/utils/port_forward.py --namespace default
PYTHONPATH=common/src python -m pytest e2e/gke_api_tests/
```

### Deploying Microservices to Cloud Run (Optional)

Run the following to build and deploy microservices to Cloud Run.
```
cd $BASE_DIR/terraform/stages/cloudrun
terraform init -backend-config=bucket=$TF_BUCKET_NAME
terraform apply -auto-approve
```

Test with API endpoint:
```
cd $BASE_DIR
export SERVICE_URL=$(gcloud run services describe "cloudrun-sample" --region=us-central1 --format="value(status.url)")
export URL="${SERVICE_URL}/sample_service/docs"
echo "Open this URL in a browser: ${URL}"
```
- When opening up the URL, you will see the Swagger frontend page with available API endpoint description.

Run API tests (Optional):
```
# Run API tests
cd $BASE_DIR
mkdir -p .test_output
gcloud run services list --format=json > .test_output/cloudrun_service_list.json
export SERVICE_LIST_JSON=.test_output/cloudrun_service_list.json
PYTHONPATH=common/src python -m pytest e2e/cloudrun_api_tests/
```

### Cleaning up all deployment and resources

Run the following to destory all deployment and resources.
> Note: there are some GCP resoureces that are not deletable, e.g. Firebase initialization.

```
cd $BASE_DIR/terraform/stages/gke
terraform destroy -auto-approve

cd $BASE_DIR/terraform/stages/cloudrun
terraform destroy -auto-approve

cd $BASE_DIR/terraform/stages/foundation
terraform destroy -auto-approve
```

## FAQ
- Who are the target audience/users for this Solutions template?
  - A: Any engineering team to start a new solution development project.
- Can I choose to deploy microservice just to Cloud Run?
  - A: Yes, please refer to `Getting Started - Setting up with setup_all script` in the README.md to choose where to deploy microservices.

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