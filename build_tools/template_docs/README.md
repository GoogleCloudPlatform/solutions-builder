# {{cookiecutter.project_name}}

> This codebase is generated from https://github.com/GoogleCloudPlatform/solutions-template

Table of Content

<!-- vscode-markdown-toc -->
* 1. [Prerequisites](#Prerequisites)
	* 1.1. [Understanding Google Cloud](#UnderstandingGoogleCloud)
	* 1.2. [Tool requirements:](#Toolrequirements:)
	* 1.3. [Install Cookiecutter ([Github](https://github.com/cookiecutter/cookiecutter)):](#InstallCookiecutterGithubhttps:github.comcookiecuttercookiecutter:)
	* 1.4. [Required packages for deploying to GKE cluster:](#RequiredpackagesfordeployingtoGKEcluster:)
	* 1.5. [Apple M1 Chip Support for Terraform (Optional)](#AppleM1ChipSupportforTerraformOptional)
* 2. [Getting Started - Setting up Google Cloud project](#GettingStarted-SettingupGoogleCloudproject)
	* 2.1. [Set up working environment:](#Setupworkingenvironment:)
	* 2.2. [Updating GCP Organizational policies](#UpdatingGCPOrganizationalpolicies)
	* 2.3. [ Setting up GCP foundation - Terraform](#SettingupGCPfoundation-Terraform)
	* 2.4. [Deploying Microservices to GKE](#DeployingMicroservicestoGKE)
	* 2.5. [Deploying Microservices to CloudRun](#DeployingMicroservicestoCloudRun)
	* 2.6. [(Optional) Manually Deploying Microservices to CloudRun](#OptionalManuallyDeployingMicroservicestoCloudRun)
* 3. [Development](#Development)
* 4. [End-to-End API tests](#End-to-EndAPItests)
* 5. [CI/CD and Test Automation](#CICDandTestAutomation)
	* 5.1. [Github Actions](#GithubActions)
	* 5.2. [Test Github Action workflows locally](#TestGithubActionworkflowslocally)
* 6. [CloudBuild](#CloudBuild)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

Please contact {{cookiecutter.admin_email}} for any questions.

> **_New Developers:_** Consult the [development guide](./DEVELOPMENT.md) for development flow and guidance

##  1. <a name='Prerequisites'></a>Prerequisites

###  1.1. <a name='UnderstandingGoogleCloud'></a>Understanding Google Cloud

We recommend the following resources to get familiar with Google Cloud and microservices.

- What is Microservice Architecture: https://cloud.google.com/learn/what-is-microservices-architecture
- Kubernetes:
  - Learn about the basics of Kubernetes: https://kubernetes.io/docs/concepts/overview/
  - Google Kubernetes Engine (GKE) overview: https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview
  - Skaffold, a command line tool that facilitates continuous development for container based & Kubernetes applications: https://skaffold.dev/docs/
- CloudRun:
  - Serverless container deployment and execution with CloudRun: https://cloud.google.com/run/docs/overview/what-is-cloud-run

###  1.2. <a name='Toolrequirements:'></a>Tool requirements:

| Tool  | Required Version  | Documentation site |
|---|---|---|
| gcloud CLI          | Latest     | https://cloud.google.com/sdk/docs/install |
| Terraform           | >= v1.3.7  | https://developer.hashicorp.com/terraform/downloads |
| Skaffold (for GKE)  | >= v2.0.4  | https://skaffold.dev/ |
| Kustomize (for GKE) | >= v4.3.1  | https://kustomize.io/ |

###  1.4. <a name='RequiredpackagesfordeployingtoGKEcluster:'></a>Required packages for deploying to GKE cluster:
> You can skip this section if you choose to deploy microservices to CloudRun only.

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

###  1.5. <a name='AppleM1ChipSupportforTerraformOptional'></a>Apple M1 Chip Support for Terraform (Optional)

If you are running commands on an Apple M1 chip Macbook, make sure run the following to add M1 support for Terraform:
```
brew install kreuzwerker/taps/m1-terraform-provider-helper
m1-terraform-provider-helper activate
m1-terraform-provider-helper install hashicorp/template -v v2.2.0
```

##  2. <a name='GettingStarted-SettingupGoogleCloudproject'></a>Getting Started - Setting up Google Cloud project

> The section covers the same setup steps as in the `README.md` generated inside **your-project-folder**.

###  2.1. <a name='Setupworkingenvironment:'></a>Set up working environment:
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

###  2.2. <a name='UpdatingGCPOrganizationalpolicies'></a>Updating GCP Organizational policies

Run the following commands to update Organization policies:
```
export ORGANIZATION_ID="$(gcloud organizations list --format="value(name)" | head -n 1)"
gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
```

Or, go to [GCP Console](https://console.cloud.google.com/iam-admin/orgpolicies) and change the following Organization policy constraints:
- constraints/compute.requireOsLogin - `Enforced Off`
- constraints/compute.vmExternalIpAccess - `Allow All`

###  2.3. <a name='SettingupGCPfoundation-Terraform'></a> Setting up GCP foundation - Terraform

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

###  2.4. <a name='DeployingMicroservicestoGKE'></a>Deploying Microservices to GKE

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

###  2.5. <a name='DeployingMicroservicestoCloudRun'></a>Deploying Microservices to CloudRun

Open `terraform/environments/dev/main.tf` and uncomment the CloudRun section like below:

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

###  2.6. <a name='OptionalManuallyDeployingMicroservicestoCloudRun'></a>(Optional) Manually Deploying Microservices to CloudRun

Build common image
```
cd common
gcloud builds submit --config=cloudbuild.yaml --substitutions=\
_PROJECT_ID="$PROJECT_ID",\
_REGION="$REGION",\
_REPOSITORY="cloudrun",\
_IMAGE="common"
```

Set up endpoint permission:
```
export SERVICE_NAME=sample-service
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

Build service image
```
gcloud builds submit --config=cloudbuild.yaml --substitutions=\
_CLOUD_RUN_SERVICE_NAME=$SERVICE_NAME,\
_PROJECT_ID="$PROJECT_ID",\
_REGION="$REGION",\
_REPOSITORY="cloudrun",\
_IMAGE="cloudrun-sample",\
_SERVICE_ACCOUNT="deployment-dev@$PROJECT_ID.iam.gserviceaccount.com",\
_ALLOW_UNAUTHENTICATED_FLAG="--allow-unauthenticated"
```

Manually deploy a microservice to CloudRun with public endpoint:
```
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

##  3. <a name='Development'></a>Development

##  4. <a name='End-to-EndAPItests'></a>End-to-End API tests

##  5. <a name='CICDandTestAutomation'></a>CI/CD and Test Automation

###  5.1. <a name='GithubActions'></a>Github Actions

###  5.2. <a name='TestGithubActionworkflowslocally'></a>Test Github Action workflows locally

- Install Docker desktop: https://www.docker.com/products/docker-desktop/
- Install [Act](https://github.com/nektos/act)
  ```
  # Mac
  brew install act

  # Windows
  choco install act-cli
  ```

- Run a specific Workflow
  ```
  act --workflows .github/workflows/e2e_gke_api_test.yaml
  ```

# Development Process & Best Practices

See the [developer guide](./DEVELOPMENT.md) for detailed development workflow
