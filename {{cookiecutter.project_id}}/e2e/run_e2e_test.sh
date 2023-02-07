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

# This script runs the e2e test with the following steps:
# - Create a new GCP project.
# - Init with env vars and other setup.
# - Run terraform apply, which create GKE cluster and other resources.
# - Run skaffold to deploy microservices.
# - Test API endpoints.

# Log in to gcloud or with a service account.
# Option 1) gcloud auth login && gcloud auth application-default login
# Option 2) gcloud auth activate-service-account $SA_EMAIL --key-file=$PATH_TO_KEY_FILE

# Usage:
# sh run_e2e_test.sh
# sh run_e2e_test.sh -n # Skip cleaning up project, for debug purpose.

# To calculate time elapsed.
SECONDS=0

# Hardcoded the project ID for all local development.
declare -a EnvVars=(
  "ORGANIZATION_ID"
  "FOLDER_ID"
  "BILLING_ACCOUNT"
  "GOOGLE_APPLICATION_CREDENTIALS"
)
for variable in ${EnvVars[@]}; do
  if [[ -z "${!variable}" ]]; then
    printf "$variable is not set.\n"
    exit -1
  fi
done

# The following vars need to be set in the environment when runnin the e2e tests.
# For example, set up env vars and action secrets in Github Action workflow.
echo "ORGANIZATION_ID=$ORGANIZATION_ID"
echo "FOLDER_ID=$FOLDER_ID"
echo "BILLING_ACCOUNT=$BILLING_ACCOUNT"
echo "GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS"

# Parsing arguments
nocleanup=""
while getopts "n" flag
do
  case "${flag}" in
    n) nocleanup="nocleanup";;
  esac
done

# Re-build template
echo yes | sh ./build_tools/build_template.sh

# Initializing E2E test environment vars
export OUTPUT_FOLDER=".test_output"
export PROJECT_ID=solutemp-e2e-$(uuidgen | head -c 8 | awk '{print tolower($0)}')
export ADMIN_EMAIL=$(gcloud auth list --filter=status:ACTIVE --format='value(account)')
pip3 install pytest --no-input
echo "PROJECT_ID=$PROJECT_ID"

### Create a new Google Cloud project:
create_new_project() {
  gcloud projects create $PROJECT_ID --folder $FOLDER_ID --quiet
  gcloud config set project $PROJECT_ID --quiet
}

install_dependencies() {
  ### Install Cookiecutter
  python3 -m pip install cookiecutter
  
  ### Create skeleton code in a new folder with Cookiecutter
  cookiecutter . --no-input -o $OUTPUT_FOLDER project_id=$PROJECT_ID admin_email=$ADMIN_EMAIL
}

setup_working_folder() {
  mkdir -p $OUTPUT_FOLDER
  
  ### Set up working environment:
  cd $OUTPUT_FOLDER/$PROJECT_ID
  export API_DOMAIN=localhost
  export BASE_DIR=$(pwd)
  echo "Current directory: ${BASE_DIR}"
  echo
}

# Test with API endpoint (GKE):
test_api_endpoints_gke() {
  # Run API e2e tests
  cd $BASE_DIR
  python3 e2e/utils/port_forward.py --namespace default
  PYTHONPATH=common/src python3 -m pytest e2e/gke_api_tests/
  GKE_PYTEST_STATUS=${PIPESTATUS[0]}
}

# Test with API endpoint (CloudRun):
test_api_endpoints_cloudrun() {
  cd $BASE_DIR
  
  # Run API e2e tests
  mkdir -p .test_output
  gcloud run services list --format=json > .test_output/cloudrun_service_list.json
  export SERVICE_LIST_JSON=.test_output/cloudrun_service_list.json
  PYTHONPATH=common/src python3 -m pytest e2e/cloudrun_api_tests/
  CLOUDRUN_PYTEST_STATUS=${PIPESTATUS[0]}
}

clean_up() {
  # Deleting project.
  echo "PROJECT_ID=${PROJECT_ID}"
  echo "Clearning up project: ${PROJECT_ID}"
  gcloud projects delete $PROJECT_ID --quiet
  # rm -rf $OUTPUT_FOLDER/$PROJECT_ID
}

# Run all steps
create_new_project
install_dependencies
setup_working_folder

# Run setup_all script to deploy to GKE and Cloud Run
export TEMPLATE_FEATURES="gke|cloudrun"
sh ./setup/setup_all.sh
test_api_endpoints_gke
test_api_endpoints_gcloud

# Cleaning up e2e test project.
if [[ "$nocleanup" ==  "" ]]; then
  printf "Cleaning up ${PROJECT_ID}...\n"
  clean_up
else
  echo "Skip project cleaning up..."
  echo
fi

echo "PROJECT_ID=$PROJECT_ID"
echo "Elapsed Time: $(expr $SECONDS / 60) minutes"

# Check API tests result
if [[ $GKE_PYTEST_STATUS == 0 && $CLOUDRUN_PYTEST_STATUS == 0 ]]; then
  echo "API Tests passed."
else
  echo -e '\033[31m ERROR: API Tests failed \033[0m'
  echo "GKE_PYTEST_STATUS=$GKE_PYTEST_STATUS"
  echo "CLOUDRUN_PYTEST_STATUS=$CLOUDRUN_PYTEST_STATUS"
  exit -1
fi
