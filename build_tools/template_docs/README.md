# {{cookiecutter.project_name}}
<!-- vscode-markdown-toc -->
* 1. [Project Requirements](#ProjectRequirements)
* 2. [Getting Started](#GettingStarted)
	* 2.1. [Prerequisites](#Prerequisites)
	* 2.2. [GCP Organizational policies](#GCPOrganizationalpolicies)
	* 2.3. [GCP Foundation Setup - Terraform](#GCPFoundationSetup-Terraform)
	* 2.4. [Deploying Kubernetes Microservices to GKE](#DeployingKubernetesMicroservicestoGKE)
	* 2.5. [Deploying Microservices to CloudRun](#DeployingMicroservicestoCloudRun)
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

> This solution skeleton is created from https://github.com/GoogleCloudPlatform/solutions-template

Please contact {{cookiecutter.admin_email}} for any questions.

> **_New Developers:_** Consult the [development guide](./DEVELOPMENT.md) for setup and contribution instructions



##  1. <a name='ProjectRequirements'></a>Project Requirements

| Tool  | Current Version  | Documentation site |
|---|---|---|
| Skaffold   | v2.x    | https://skaffold.dev/ |
| Kustomize  | v4.3.1  | https://kustomize.io/ |
| gcloud CLI | Latest  | https://cloud.google.com/sdk/docs/install |

##  2. <a name='GettingStarted'></a>Getting Started

This guide will detail how to set up your new solutions template project. See the [development guide](./DEVELOPMENT.md) for how to contribute to the project.

###  2.1. <a name='Prerequisites'></a>Prerequisites

```
# Set up environmental variables
export PROJECT_ID={{cookiecutter.project_id}}
export ADMIN_EMAIL={{cookiecutter.admin_email}}
export REGION={{cookiecutter.gcp_region}}
export API_DOMAIN={{cookiecutter.api_domain}}
export BASE_DIR=$(pwd)

# Login to Google Cloud
gcloud auth application-default login
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID
```

For development with Kubernetes on GKE:

Install required packages:

- For MacOS:
  ```
  brew install --cask skaffold kustomize google-cloud-sdk
  ```

- For Windows:
  ```
  choco install -y skaffold kustomize gcloudsdk
  ```

- For Linux/Ubuntu:
  ```
  curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
  sudo install skaffold /usr/local/bin/
  ```

* Make sure to use __skaffold 1.24.1__ or later for development.

###  2.2. <a name='GCPOrganizationalpolicies'></a>GCP Organizational policies

Optionally, you may need to update Organization policies for CI/CD test automation.

Run the following commands to update Organization policies:
```
export ORGANIZATION_ID=$(gcloud organizations list --format="value(name)")
gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
```

Or, change the following Organization policy constraints in [GCP Console](https://console.cloud.google.com/iam-admin/orgpolicies)
- constraints/compute.requireOsLogin - Enforced Off
- constraints/compute.vmExternalIpAccess - Allow All

###  2.3. <a name='GCPFoundationSetup-Terraform'></a>GCP Foundation Setup - Terraform

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

Run Terraform apply

```
# Init Terraform
cd terraform/environments/dev
terraform init -backend-config=bucket=$TF_BUCKET_NAME

# Enabling GCP services first.
terraform apply -target=module.project_services -target=module.service_accounts -auto-approve

# Initializing Firebase (if using Firestore)
# NOTE: the Firebase can only be initialized once (via App Engine).
terraform apply -target=module.firebase -var="firebase_init=true" -auto-approve

# Run the rest of Terraform
terraform apply -auto-approve
```

###  2.4. <a name='DeployingKubernetesMicroservicestoGKE'></a>Deploying Kubernetes Microservices to GKE

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

TBD

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

##  6. <a name='CloudBuild'></a>CloudBuild

TBD

# Development Process & Best Practices

See the [developer guide](./DEVELOPMENT.md) for detailed development workflow
