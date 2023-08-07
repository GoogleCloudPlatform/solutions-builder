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

# This script sets up environment variables for bootstrapping the project, which include
# terraform service account and a bastion host for the subsequent stages

# TODO: Set Project ID and other variables
export PROJECT_ID=<your-project-id>
export DOMAIN_NAME=<your-org-domain>
export REGION=<your-region>
export ZONE=<your-zone>
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
export BILLING_ACCOUNT="$(gcloud beta billing projects describe ${PROJECT_ID} | grep billingAccountName \
    | tr / ' ' | cut -f3 -d' ')"

echo
echo "PROJECT_ID      = ${PROJECT_ID}"
echo "PROJECT_NUMBER  = ${PROJECT_NUMBER}"
echo "BILLING_ACCOUNT = ${BILLING_ACCOUNT}"
echo "REGION          = ${REGION}"
echo "ZONE            = ${ZONE}"
echo "DOMAIN_NAME     = ${DOMAIN_NAME}"
echo

# Pass variables to terraform using environment prefix TF_VAR_
export TF_VAR_project_id=${PROJECT_ID}
export TF_VAR_billing_account=${BILLING_ACCOUNT}
export TF_VAR_region=${REGION}
export TF_VAR_zone=${ZONE}
export TF_VAR_bucket_region_or_multiregion="US"
export TF_VAR_org_domain_name=${DOMAIN_NAME}
export TF_VAR_add_project_owner=true
