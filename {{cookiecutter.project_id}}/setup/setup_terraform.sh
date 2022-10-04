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

declare -a EnvVars=(
  "PROJECT_ID"
  "ADMIN_EMAIL"
  "TF_BUCKET_NAME"
  "TF_BUCKET_LOCATION"
)
for variable in ${EnvVars[@]}; do
  if [[ -z "${!variable}" ]]; then
    input_value=""
    while [[ -z "$input_value" ]]; do
      read -p "Enter the value for ${variable}: " input_value
      declare "${variable}=$input_value"
    done
  fi
done

BLUE=$(tput setaf 4)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)

create_bucket () {
  printf "PROJECT_ID=${PROJECT_ID}\n"
  printf "TF_BUCKET_NAME=${TF_BUCKET_NAME}\n"
  printf "TF_BUCKET_LOCATION=${TF_BUCKET_LOCATION}\n"

  print_highlight "Creating terraform state bucket: ${TF_BUCKET_NAME}\n"
  gsutil mb -l $TF_BUCKET_LOCATION gs://$TF_BUCKET_NAME
  gsutil versioning set on gs://$TF_BUCKET_NAME
  export TF_BUCKET_NAME=$TF_BUCKET_NAME
  echo
}

enable_apis () {
  gcloud services enable iamcredentials.googleapis.com
}

print_highlight () {
  printf "${BLUE}$1${NORMAL}\n"
}

enable_apis
create_bucket

print_highlight "Terraform state bucket: ${TF_BUCKET_NAME}\n"
