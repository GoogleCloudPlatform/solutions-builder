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

# This script contains the sequence of steps to be executed on the bastion host
# - Clone github repos
# - Authenticate to google cloud
# - Setup environment variables
# - Execute terraform to create GKE cluster for running CLP

############################################################################################################
# LOCAL MACHINE Instructions (Post bootstrapping the project)
# -----------------------------------------------------------

# Copy bootstrap terraform state to tfstate-bucket
gsutil cp ../project_bootstrap/terraform.tfstate gs://"${PROJECT_ID}"-tfstate/env/bootstrap/terraform.tfstate

# Enable deletion protection for the jump host
gcloud compute instances update jump-host --deletion-protection --project="${PROJECT_ID}"

# SCP startup script to jump host
gcloud compute scp ../scripts/bastion_startup.sh jump-host:~ --zone=${ZONE} --tunnel-through-iap --project="${PROJECT_ID}"

# Log onto the jump host using IAP and start tmux
gcloud compute ssh jump-host --zone=${ZONE} --tunnel-through-iap --project="${PROJECT_ID}"

############################################################################################################
# BASTION/JUMP HOST Instructions
# ------------------------------
# Run the startup script (takes about 10 min)
source ~/bastion_startup.sh

tmux # Preferred so that disconnected sessions are not lost (https://tmuxcheatsheet.com/)
     # To re-connect tmux attach

# Git Clone CLP repos
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git config --global credential.https://github.com.username "username"

git config --global credential.helper store
git clone https://github.com/GoogleCloudPlatform/cloud-learning-platform.git

# TODO: Set Project ID and other variables
export PROJECT_ID=<your-project-id>
export LDAP=<your-ldap>
export GITHUB_ID=<your-github-id>
export REGION=<your-region>
export ZONE=<your-zone>
export DEMO_VERSION=v2.0.0-beta12.7-demo

# Authenticate to Google Cloud
gcloud auth login
gcloud auth application-default login

# Create and download service key for terraform account
export SA_KEY_FILE=~/clp-terraform-cicd-key.json
gcloud iam service-accounts keys create ${SA_KEY_FILE} \
    --iam-account=terraform-cicd@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=${SA_KEY_FILE}

# options for firestore: https://cloud.google.com/appengine/docs/locations
# us-central1 and europe-west1 must be us-central and europe-west for legacy reasons
export TF_VAR_project_id=${PROJECT_ID}
export TF_VAR_region=${REGION}
export TF_VAR_firestore_region="us-central"
export TF_VAR_gke_cluster_zones=${ZONE}
export TF_VAR_github_owner=${GITHUB_ID}
export TF_VAR_api_domain="${PROJECT_ID}-api"
export TF_VAR_web_app_domain="${PROJECT_ID}"
export TF_VAR_ckt_app_domain="${PROJECT_ID}-ckt"
export TF_VAR_github_ref="refs/tags/${DEMO_VERSION}"

# TODO: External projects need to set these appropriately
# These variables have been defaulted for Argolis projects
export TF_VAR_cert_issuer_email="${LDAP}@google.com"
export TF_VAR_org_domain_name="${LDAP}.altostrat.com"
export TF_VAR_base_domain="cloudpssolutions.com"
export TF_VAR_ai_tutor_whitelist_domains="google.com"
export TF_VAR_ai_tutor_whitelist_emails="${LDAP}@google.com,admin@${LDAP}.altostrat.com"
export TF_VAR_ckt_whitelist_domains="google.com"
export TF_VAR_ckt_whitelist_emails="${LDAP}@google.com,admin@${LDAP}.altostrat.com"

# TODO: Backward compatibility changes
# Comment out the following for existing customer deployments
export TF_VAR_existing_custom_vpc="true"

# Create main GKE cluster for installing backend services
pushd cloud-learning-platform/terraform
cd stages/demo_environment

terraform init -backend-config="bucket=${PROJECT_ID}-tfstate"
terraform plan | grep -e "#"

# Firestore may only be initialized once
FIRESTORE_INIT="-var=firebase_init=false"
if [[ $(gcloud alpha firestore databases list --project="${PROJECT_ID}" --quiet | grep -c uid) == 0 ]]; then
  FIRESTORE_INIT="-var=firebase_init=true"
fi

terraform apply ${FIRESTORE_INIT} --auto-approve
popd
