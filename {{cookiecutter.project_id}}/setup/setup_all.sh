#!/bin/bash
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script automates all the setup steps after creating code skeleton using
# the Solutions template and set up all components to a brand-new Google Cloud
# project.

# Setting up environment variables.
setup_env_vars() {
  export PROJECT_ID="{{cookiecutter.project_id}}"
  export ADMIN_EMAIL="{{cookiecutter.admin_email}}"
  export REGION="{{cookiecutter.gcp_region}}"
  export TF_VAR_project_id=$PROJECT_ID
  export TF_VAR_api_domain=$API_DOMAIN
  export TF_VAR_web_app_domain=$API_DOMAIN
  export TF_VAR_admin_email=$ADMIN_EMAIL
  export TF_BUCKET_NAME="${PROJECT_ID}-tfstate"
  export TF_BUCKET_LOCATION="us"
  export BASE_DIR=$(pwd)
}

# Setting up gcloud CLI
setup_gcloud() {
  gcloud config set project $PROJECT_ID --quiet
  gcloud components install gke-gcloud-auth-plugin --quiet
}

# Updating GCP Organizational policies
update_gcp_org_policies() {
  if [[ "$ORGANIZATION_ID" ==  "" ]]; then
    export ORGANIZATION_ID="$(gcloud organizations list --format='value(name)' | head -n 1)"
  fi
  echo "Updating orgniazation policies: ORGANIZATION_ID=$ORGANIZATION_ID"
  gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --organization=$ORGANIZATION_ID
  gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --organization=$ORGANIZATION_ID
  gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
}

# Grant Storage admin to the current user IAM.
grant_storage_iam() {
  export CURRENT_USER=$(gcloud config list account --format "value(core.account)" | head -n 1)
  gcloud config set project $PROJECT_ID --quiet
  gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$CURRENT_USER" --role='roles/storage.admin' --quiet
  sleep 3s
}

# Link billing account to the current project.
link_billing_account() {
  if [[ "$BILLING_ACCOUNT" ==  "" ]]; then
    export BILLING_ACCOUNT=$(gcloud beta billing accounts list --format "value(name)" | head -n 1)
  fi
  echo "Linking billing account to $PROJECT: BILLING_ACCOUNT=$BILLING_ACCOUNT"
  gcloud beta billing projects link $PROJECT_ID --billing-account $BILLING_ACCOUNT --quiet
}

# Create Terraform Statefile in GCS bucket.
create_terraform_gcs_bucket() {
  bash setup/setup_terraform.sh
  
  # List all buckets.
  gcloud storage ls
  echo "TF_BUCKET_NAME = ${TF_BUCKET_NAME}"
  echo
}

# Run terraform to set up all GCP resources. (Setting up GKE by default)
init_foundation() {
  # Init Terraform
  cd terraform/stages/foundation
  terraform init -reconfigure -backend-config=bucket=$TF_BUCKET_NAME
  
  # Enabling GCP services first.
  terraform apply -target=module.project_services -target=module.service_accounts -auto-approve
  
  # Initializing Firebase (Only need this for the first time.)
  # NOTE: the Firebase can only be initialized once (via App Engine).
  terraform apply -target=module.firebase -var="firebase_init=true" -auto-approve
  
  # Run the rest of Terraform
  terraform apply -auto-approve
}

# Build all microservices and deploy to the cluster:
deploy_microservices_to_gke() {
  cd $BASE_DIR/terraform/stages/gke
  terraform init -backend-config=bucket=$TF_BUCKET_NAME
  terraform apply -auto-approve
  
  cd $BASE_DIR
  export CLUSTER_NAME=main-cluster
  gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION --project $PROJECT_ID
  skaffold run -p prod --default-repo=gcr.io/$PROJECT_ID
}

# Build all microservices and deploy to CloudRun:
deploy_microservices_to_cloudrun() {
  cd $BASE_DIR/terraform/stages/cloudrun
  terraform init -backend-config=bucket=$TF_BUCKET_NAME
  terraform apply -auto-approve
}

# Test with API endpoint (GKE):
test_api_endpoints_gke() {
  # Run API e2e tests
  export API_DOMAIN=$(kubectl describe ingress | grep Address | awk '{print $2}')
  export URL="http://${API_DOMAIN}/sample_service/docs"
  echo "The API endpoints are ready. See the auto-generated API docs at this URL: ${URL}"
}

# Test with API endpoint (CloudRun):
test_api_endpoints_cloudrun() {
  # Run API e2e tests
  export SERVICE_URL=$(gcloud run services describe "cloudrun-sample" --region={{cookiecutter.gcp_region}} --format="value(status.url)")
  export URL="${SERVICE_URL}/sample_service/docs"
  echo "The API endpoints are ready. See the auto-generated API docs at this URL: ${URL}"
}

setup_env_vars
setup_gcloud
update_gcp_org_policies
grant_storage_iam
link_billing_account
create_terraform_gcs_bucket
init_foundation

if [[ "$TEMPLATE_FEATURES" ==  "gke" ]]; then
  printf "Deploying microservices to GKE...\n"
  deploy_microservices_to_gke
  test_api_endpoints_gke
fi

if [[ "$TEMPLATE_FEATURES" ==  "cloudrun" ]]; then
  printf "Deploying microservices to CloudRun...\n"
  deploy_microservices_to_cloudrun
  test_api_endpoints_cloudrun
fi
  deploy_microservices_to_cloudrun
  test_api_endpoints_cloudrun
fi
