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

# To calculate time elapsed.
SECONDS=0

# Parsing arguments
nocleanup=""
while getopts "n" flag
do
  case "${flag}" in
    -n) nocleanup="nocleanup";;
  esac
done

# Initializing E2E test environment vars
export OUTPUT_FOLDER=".e2e_test_output"
export PROJECT_ID=solutemp-e2e-$(uuidgen | head -c 8 | awk '{print tolower($0)}')
export ADMIN_EMAIL=$(gcloud auth list --filter=status:ACTIVE --format='value(account)')

### Create a new Google Cloud project:
create_new_project() {
  export ORGANIZATION_ID="$(gcloud organizations list --format='value(name)' | head -n 1)"
  gcloud projects create $PROJECT_ID --organization $ORGANIZATION_ID --quiet
  gcloud config set project $PROJECT_ID --quiet
}

install_dependencies() {
  ### Install Cookiecutter
  python3 -m pip install cookiecutter
  
  ### Create skeleton code in a new folder with Cookiecutter
  cookiecutter . --no-input -o $OUTPUT_FOLDER project_id=$PROJECT_ID
}

setup_working_folder() {
  mkdir -p $OUTPUT_FOLDER
  echo "PROJECT_ID = $PROJECT_ID"
  echo "ADMIN_EMAIL = $ADMIN_EMAIL"
  
  ### Set up working environment:
  export REGION={{cookiecutter.gcp_region}}
  export API_DOMAIN=localhost
  
  cd $OUTPUT_FOLDER/$PROJECT_ID
  export BASE_DIR=$(pwd)
  echo "Current directory: ${BASE_DIR}"
  echo
}

clean_up() {
  ### Clean up
  echo "PROJECT_ID=${PROJECT_ID}"
  echo "Clearning up project: ${PROJECT_ID}"
  gcloud projects delete $PROJECT_ID --quiet
  # rm -rf $OUTPUT_FOLDER/$PROJECT_ID
}

# Run all steps
create_new_project
install_dependencies
setup_working_folder

# Run setup_all script to perform all other steps.
chmod 755 ./setup/setup_all.sh
sh ./setup/setup_all.sh

if [[ "$nocleanup" ==  "" ]]; then
  printf "Cleaning up ${PROJECT_ID}...\n"
  clean_up
else
  echo "Skipping clean up."
fi

echo "PROJECT_ID=$PROJECT_ID"
echo "Elapsed Time: $(expr $SECONDS / 60) minutes"

if [[ $PYTEST_STATUS -ne 0 ]]; then
  echo "ERROR: pytest failed, exiting ..."
  exit $PYTEST_STATUS
fi
