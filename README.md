# Google Cloud Solutions Template

> A template to generate a new project with built-in structure and features
> to accelerate your project setup.

## TL;DR

Solutions Template is a boilerplate template for building repeatable
solutions with the best practices in architecture on Google Cloud, including GKE
clusters, Test Automation, CI/CD, as well as development process.

This template provides built-in and ready-to-ship sample features including:
* Kubernetes-based microservices
* Simplified deployment using Skaffold and Kustomize
* Terraform Google Cloud foundation setup
* CI/CD deployment (with Github Actions)
* CloudRun templates
* [In Progress] CI/CD deployment with CloudBuild

## Roadmap

Please see Feature Requests in the Github issue list at https://github.com/GoogleCloudPlatform/solutions-template/issues?q=is%3Aopen+is%3Aissue+label%3A%22feature+request%22

## Getting Started - Creating Solution Skeleton

### Prerequisites

Install Cookiecutter ([Github](https://github.com/cookiecutter/cookiecutter)):
- For MacOS:
  ```
  brew install cookiecutter
  ```

- For Windows, refer this [installation guide](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter)

Project requirements:

| Tool  | Required Version  | Documentation site |
|---|---|---|
| Skaffold   | >= v2.0.4  | https://skaffold.dev/ |
| Kustomize  | >= v4.3.1  | https://kustomize.io/ |
| gcloud CLI | Latest     | https://cloud.google.com/sdk/docs/install |

### Create skeleton code in a new folder with Cookiecutter

Run the following to generate skeleton code in a new folder:
```
cookiecutter https://github.com/GoogleCloudPlatform/solutions-template.git
```

Provide the required variables to Cookiecutter prompt, e.g.:
```
project_id: my-project-id
project_name [My Awesome Project]:
project_short_description [My Awesome Project]:
project_slug [my_project]:
Google Cloud_region [us-central1]:
version [0.1.0]:
admin_email [admin@example.com]:
```
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

- **README.md** - This contains all details regarding the development and deployment for your particular project.
- **skaffold.yaml** - This is the master Skaffold YAML file that defines how everything is built and deployed, depending on different profiles.
- **microservices** - The main directory for all microservices, can be broken down into individual folder for each microservie, e.g. `sample_service`.
  - [**microservice subfolder**] - Each microservice folder is a Docker container with [Skaffold](https://skaffold.dev/) + [Kustomize](https://kustomize.io/) to build images in different environments.
- **common** - The common image contains shared data models and util libraries used by all other microservices.


## Getting Started - Setting up Google Cloud project

Once the solution skeleton code generated in **your-project-folder** folder, the next step is to set up the Google Cloud project.
You will also find the same steps in the `README.md` inside **your-project-folder**.

This guide will detail how to set up your new solutions template project. See the [development guide](./DEVELOPMENT.md) for how to contribute to the project.

### Prerequisites

```
# Set up environmental variables
export PROJECT_ID=<your-project-id>
export ADMIN_EMAIL=<your-email>
export REGION=us-central1
export API_DOMAIN=example.com
export BASE_DIR=$(pwd)

# Login to Google Cloud (if not on Cloud Shell)
gcloud auth application-default login
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID
```

### Updating GCP Organizational policies

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

Run Terraform apply

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
  export SKAFFOLD_VERSION=v2.0.4
  curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/$SKAFFOLD_VERSION/skaffold-linux-amd64 && \
  sudo install skaffold /usr/local/bin/
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

## FAQ

- Who are the target audience/users for this Solutions template?
  - A: Any engineering team to start a new solution development project.

- Can I choose to deploy microservice just to CloudRun?
  - A: Yes, please follow steps in the README.md in **your-project-folder** generated from cookiecutter.
