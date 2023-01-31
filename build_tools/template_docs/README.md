# {{cookiecutter.project_name}}

> This codebase is generated from https://github.com/GoogleCloudPlatform/solutions-template

Table of Content

<!-- vscode-markdown-toc -->
* 1. [Prerequisites](#Prerequisites)
	* 1.1. [Understanding Google Cloud](#UnderstandingGoogleCloud)
	* 1.2. [Tool requirements:](#Toolrequirements:)
	* 1.3. [Required packages for deploying to GKE cluster:](#RequiredpackagesfordeployingtoGKEcluster:)
	* 1.4. [Apple M1 Chip Support for Terraform (Optional)](#AppleM1ChipSupportforTerraformOptional)
	* 1.5. [File structure](#Filestructure)
* 2. [Setting up Google Cloud Project](#SettingupGoogleCloudProject)
* 3. [Setting up Google Cloud Project (Manual Steps)](#SettingupGoogleCloudProjectManualSteps)
	* 3.1. [Set up working environment:](#Setupworkingenvironment:)
	* 3.2. [Updating GCP Organizational policies](#UpdatingGCPOrganizationalpolicies)
	* 3.3. [ Setting up GCP foundation - Terraform](#SettingupGCPfoundation-Terraform)
	* 3.4. [Deploying Microservices to GKE (Optional)](#DeployingMicroservicestoGKEOptional)
	* 3.5. [Deploying Microservices to Cloud Run (Optional)](#DeployingMicroservicestoCloudRunOptional)
	* 3.6. [(Optional) Manually Deploying Microservices to CloudRun](#OptionalManuallyDeployingMicroservicestoCloudRun)
	* 3.7. [Cleaning up all deployment and resources](#Cleaningupalldeploymentandresources)
* 4. [Development](#Development)
* 5. [End-to-End API tests](#End-to-EndAPItests)
* 6. [CI/CD and Test Automation](#CICDandTestAutomation)
	* 6.1. [Github Actions](#GithubActions)
	* 6.2. [Test Github Action workflows locally](#TestGithubActionworkflowslocally)

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

###  1.3. <a name='RequiredpackagesfordeployingtoGKEcluster:'></a>Required packages for deploying to GKE cluster:
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

###  1.4. <a name='AppleM1ChipSupportforTerraformOptional'></a>Apple M1 Chip Support for Terraform (Optional)

If you are running commands on an Apple M1 chip Macbook, make sure run the following to add M1 support for Terraform:
```
brew install kreuzwerker/taps/m1-terraform-provider-helper
m1-terraform-provider-helper activate
m1-terraform-provider-helper install hashicorp/template -v v2.2.0
```

###  1.5. <a name='Filestructure'></a>File structure

```
{{cookiecutter.project_name}}/
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

- **README.md** - General info and setup guide.
- **DEVELOPMENT.md** - Development best practices, code submission flow, and other guidances.
- **skaffold.yaml** - The master Skaffold YAML file that defines how everything is built and deployed, depending on different profiles.
- **microservices** - The main directory for all microservices, can be broken down into individual folder for each microservie, e.g. `sample_service`.
  - [**microservice subfolder**] - Each microservice folder is a Docker container with [Skaffold](https://skaffold.dev/) + [Kustomize](https://kustomize.io/) to build images in different environments.
- **common** - The common image contains shared data models and util libraries used by all other microservices.
- **.github** - Github workflows including tests and CI/CD.

##  2. <a name='SettingupGoogleCloudProject'></a>Setting up Google Cloud Project

> (Optional) check out the README.md in **your-project-folder** to check out the manual setup steps.

```
# Set up environmental variables
cd <my-gcp-project-id>
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

Once microservice deployed successfully, you will see the message below:
```
The API endpoints are ready. See the auto-generated API docs at this URL: https://<your-sample-domain>/sample_service/docs
```

##  3. <a name='SettingupGoogleCloudProjectManualSteps'></a>Setting up Google Cloud Project (Manual Steps)

###  3.1. <a name='Setupworkingenvironment:'></a>Set up working environment:

Please make sure you are at the generated folder **your-project-folder**

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

###  3.2. <a name='UpdatingGCPOrganizationalpolicies'></a>Updating GCP Organizational policies

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

###  3.3. <a name='SettingupGCPfoundation-Terraform'></a> Setting up GCP foundation - Terraform

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

###  3.4. <a name='DeployingMicroservicestoGKEOptional'></a>Deploying Microservices to GKE (Optional)

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

Verify API endpoint:
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

###  3.5. <a name='DeployingMicroservicestoCloudRunOptional'></a>Deploying Microservices to Cloud Run (Optional)

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

###  3.6. <a name='OptionalManuallyDeployingMicroservicestoCloudRun'></a>(Optional) Manually Deploying Microservices to CloudRun

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

###  3.7. <a name='Cleaningupalldeploymentandresources'></a>Cleaning up all deployment and resources

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

##  4. <a name='Development'></a>Development

##  5. <a name='End-to-EndAPItests'></a>End-to-End API tests

##  6. <a name='CICDandTestAutomation'></a>CI/CD and Test Automation

###  6.1. <a name='GithubActions'></a>Github Actions

###  6.2. <a name='TestGithubActionworkflowslocally'></a>Test Github Action workflows locally

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
