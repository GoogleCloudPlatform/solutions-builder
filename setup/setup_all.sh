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
  export PROJECT_ID="solutions-template-e2etest"
  export ADMIN_EMAIL="your_email@example.com"
  export REGION="us-central1"
  export API_DOMAIN="localhost"
  export TF_VAR_project_id=${PROJECT_ID}
  export TF_VAR_api_domain=${API_DOMAIN}
  export TF_VAR_web_app_domain=${API_DOMAIN}
  export TF_VAR_admin_email=${ADMIN_EMAIL}
  export TF_BUCKET_NAME="${PROJECT_ID}-tfstate"
  export TF_BUCKET_LOCATION="us"
  export BASE_DIR=$(pwd)
}

# Setting up gcloud CLI
setup_gcloud() {
  gcloud config set project ${PROJECT_ID} --quiet
  gcloud components install gke-gcloud-auth-plugin --quiet
  gcloud services enable cloudresourcemanager.googleapis.com --quiet
}

# Updating GCP Organizational policies
update_gcp_org_policies() {
  if [[ "${ORGANIZATION_ID}" == "" ]]; then
    export ORGANIZATION_ID="$(gcloud organizations list --format='value(name)' | head -n 1)"
  fi
  echo "Updating organization policies: ORGANIZATION_ID=${ORGANIZATION_ID}"
  gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --organization="${ORGANIZATION_ID}"
  gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --organization="${ORGANIZATION_ID}"
  gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization="${ORGANIZATION_ID}"
}

# Create a Service Account for Terraform impersonating and grant Storage admin to the current user IAM.
setup_service_accounts_and_iam() {
  export CURRENT_USER=$(gcloud config list account --format "value(core.account)" | head -n 1)
  # Check if the current user is a service account.
  if [[ "$CURRENT_USER" == *"iam.gserviceaccount.com"* ]]; then
    MEMBER_PREFIX="serviceAccount"
  else
    MEMBER_PREFIX="user"
  fi
  
  # Create TF runner services account and use it for impersonate.
  export TF_RUNNER_SA_EMAIL="terraform-runner@${PROJECT_ID}.iam.gserviceaccount.com"
  export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=${TF_RUNNER_SA_EMAIL}
  gcloud iam service-accounts create "terraform-runner"
  
  # Grant service account Token creator for current user.
  declare -a runnerRoles=(
    "roles/iam.serviceAccountTokenCreator"
    "roles/iam.serviceAccountUser"
  )
  for role in "${runnerRoles[@]}"; do
    gcloud iam service-accounts add-iam-policy-binding ${TF_RUNNER_SA_EMAIL} --member="$MEMBER_PREFIX:$CURRENT_USER" --role="$role"
  done
  
  # Bind the TF runner service account with required roles.
  declare -a runnerRoles=(
    "roles/owner"
    "roles/storage.admin"
  )
  for role in "${runnerRoles[@]}"; do
    gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${TF_RUNNER_SA_EMAIL}" --role="$role" --quiet
  done
}

# Link billing account to the current project.
link_billing_account() {
  if [[ "${BILLING_ACCOUNT}" == "" ]]; then
    export BILLING_ACCOUNT=$(gcloud beta billing accounts list --format "value(name)" | head -n 1)
  fi
  echo "Linking billing account to ${PROJECT_ID}: BILLING_ACCOUNT=${BILLING_ACCOUNT}"
  gcloud beta billing projects link ${PROJECT_ID} --billing-account "${BILLING_ACCOUNT}" --quiet
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
  cd "$BASE_DIR"/terraform/stages/foundation
  terraform init -reconfigure -backend-config=bucket=${TF_BUCKET_NAME}
  
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
  cd "$BASE_DIR"/terraform/stages/gke
  terraform init -backend-config=bucket=${TF_BUCKET_NAME}
  terraform apply -auto-approve
  
  cd "$BASE_DIR"
  export CLUSTER_NAME=main-cluster
  gcloud container clusters get-credentials ${CLUSTER_NAME} --region $REGION --project ${PROJECT_ID}
  skaffold run -p prod --default-repo=gcr.io/${PROJECT_ID}
}

# Build all microservices and deploy to CloudRun:
deploy_microservices_to_cloudrun() {
  cd "$BASE_DIR"/terraform/stages/cloudrun
  terraform init -backend-config=bucket=${TF_BUCKET_NAME}
  terraform apply -auto-approve
}

# Test with API endpoint (GKE):
test_api_endpoints_gke() {
  # Run API e2e tests
  API_DOMAIN=$(kubectl describe ingress | grep Address | awk '{print $2}')
  URL="http://${API_DOMAIN}/sample_service/docs"
  GKE_OUTPUT="The API endpoints are ready. See the auto-generated API docs at this URL: ${URL}"
}

# Test with API endpoint (CloudRun):
test_api_endpoints_cloudrun() {
  # Run API e2e tests
  SERVICE_URL=$(gcloud run services describe "cloudrun-sample" --region=us-central1 --format="value(status.url)")
  URL="${SERVICE_URL}/sample_service/docs"
  CLOUDRUN_OUTPUT="The API endpoints are ready. See the auto-generated API docs at this URL: ${URL}"
}

setup_env_vars
setup_gcloud
update_gcp_org_policies
link_billing_account
setup_service_accounts_and_iam
create_terraform_gcs_bucket

echo "Wait 10 seconds for IAM updates..."
sleep 10
init_foundation

final_message=""

# Checking all Template features, using "|: as delimiter.
IFS='|' read -a strarr <<< "$TEMPLATE_FEATURES"
for feature in "${strarr[@]}";
do
  echo "feature=$feature"
  case $feature in
    "gke")
      printf "Deploying microservices to GKE...\n"
      deploy_microservices_to_gke
      test_api_endpoints_gke
      final_message+=$GKE_OUTPUT$'\n\n'
      ;;
    "cloudrun")
      printf "Deploying microservices to CloudRun...\n"
      deploy_microservices_to_cloudrun
      test_api_endpoints_cloudrun
      final_message+=$CLOUDRUN_OUTPUT$'\n\n'
      ;;
  esac
done

echo $'Setup complete, see the deployment info below:\n\n'
echo "$final_message"
