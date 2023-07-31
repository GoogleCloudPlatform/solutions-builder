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
# the Solutions Builder and set up all components to a brand-new Google Cloud
# project.

export PROJECT_ID="{{project_id}}"
export REGION="{{gcp_region}}"

{% if deploy_with_gke == true -%}
export CLUSTER_NAME=main-cluster
{%- endif %}

# # Terraform impersonate service account
# export TF_RUNNER_SA_EMAIL="terraform-runner@$PROJECT_ID.iam.gserviceaccount.com"
# export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=$TF_RUNNER_SA_EMAIL
