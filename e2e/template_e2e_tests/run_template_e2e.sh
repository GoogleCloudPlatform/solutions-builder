# #!/bin/bash
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

#!/bin/bash

declare -a EnvVars=(
  "PROJECT_ID"
  "REGION"
)
for variable in "${EnvVars[@]}"; do
  if [[ -z "${!variable}" ]]; then
    printf "$variable is not set.\n"
    exit 1
  fi
done

export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

# Create new solution folder
st new $PROJECT_ID --answers=\
project_id=$PROJECT_ID,\
project_name=$PROJECT_ID,\
project_number=$PROJECT_NUMBER,\
gcp_region=$REGION,\
terraform_backend_gcs=Y,\
advanced_settings=n

# Add RESTful service component
cd $PROJECT_ID
st component add restful_service --answers=\
component_name=todo_service,\
resource_name=todo-service,\
service_path=todo-service,\
gcp_region=$REGION,\
data_model=todo,\
data_model_plural=todos,\
deploy_cloudrun=Y,\
cloudrun_neg=Y,\
deploy_gke=n,\
default_deploy=cloudrun,\
depend_on_common=n,\
local_port=9001,\
use_github_action=Y \
--yes

# Initialize infra, but skipping the bootstrap stage.
# st infra apply 1-boostrap --yes
st infra apply 2-foundation --yes

# Deploy to Cloud Run
st deploy --yes

# Run Pytest for E2E API calls.
pytest tests/e2e/
PYTEST_STATUS=${PIPESTATUS[0]}

# Clean up
st destroy --yes
st infra destroy 2-foundation --yes

# Return error status if pytest not passed.
if [[ $PYTEST_STATUS != 0 ]]; then
  exit 1
fi
