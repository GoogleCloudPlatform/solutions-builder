#!/bin/bash
# Copyright 2023 Google LLC
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

#!/bin/bash

set -f

# Hardcoded the project ID for all local development.
declare -a EnvVars=(
  "SA_EMAIL"
)
for variable in "${EnvVars[@]}"; do
  if [[ -z "${!variable}" ]]; then
    printf "$variable is not set.\n"
    exit 1
  fi
done

mkdir -p .tmp
gcloud iam service-accounts keys create .tmp/sa-key.json --iam-account=$SA_EMAIL

gcloud auth activate-service-account --key-file=.tmp/sa-key.json
then
  PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

  # Create new solution folder
  sb new $PROJECT_ID $OUTPUT_FOLDER --answers=project_id=$PROJECT_ID,project_name=$PROJECT_ID,project_number=$PROJECT_NUMBER,gcp_region=$REGION,terraform_backend_gcs=Y,advanced_settings=n

  # Add RESTful service component
  cd $OUTPUT_FOLDER/$PROJECT_ID
  sb components add restful_service --answers=component_name=todo_service,resource_name=todo-service,service_path=todo-service,gcp_region=$REGION,data_model=todo,data_model_plural=todos,deploy_cloudrun=Y,cloudrun_neg=Y,deploy_gke=n,default_deploy=cloudrun,depend_on_common=n,local_port=9001,use_github_action=Y --yes

  # Initialize infra, but skipping the bootstrap stage.
  # sb infra apply 1-boostrap --yes
  sb infra apply 2-foundation --yes

elif [[ $1 = "deploy" ]]
then
  # Deploy to Cloud Run
  cd $OUTPUT_FOLDER/$PROJECT_ID
  ls -al .
  sb deploy --yes

elif [[ $1 = "test" ]]
then
  # Run Pytest for E2E API calls.
  cd $OUTPUT_FOLDER/$PROJECT_ID
  ls -al .
  ls -al tests/e2e/
  PYTHONPATH=. pytest tests/e2e/

elif [[ $1 = "cleanup" ]]
then
  # Clean up
  cd $OUTPUT_FOLDER/$PROJECT_ID
  sb destroy --yes
  sb infra destroy 2-foundation --yes

else
  echo "Usage: bash run_template_e2e.sh [prepare|deploy|test|cleanup]"
fi
