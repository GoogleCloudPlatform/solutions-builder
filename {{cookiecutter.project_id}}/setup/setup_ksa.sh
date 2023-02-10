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

set -e

declare -a EnvVars=(
  "NAMESPACE"
  "PROJECT_ID"
)

for variable in "${EnvVars[@]}"; do
  if [[ -z "${!variable}" ]]; then
    printf "%s is not set.\n" "$variable"
    exit 1
  fi
done

GSA_NAME="gke-pod-sa"
KSA_NAME="ksa"

echo
echo "NAMESPACE=${NAMESPACE}"
echo "PROJECT_ID=${PROJECT_ID}"
echo

declare EXISTING_KSA=$(kubectl get sa -n "${NAMESPACE}" | egrep -i "^${KSA_NAME} ")
printf "\nCreating kubernetes service account on the cluster ...\n"
if [[ "$EXISTING_KSA" = "" ]]; then
  kubectl create serviceaccount -n "${NAMESPACE}" ${KSA_NAME}
fi

printf "\nAdding Service Account IAM policy ...\n"
gcloud iam service-accounts add-iam-policy-binding \
--role roles/iam.workloadIdentityUser \
--member "serviceAccount:${PROJECT_ID}.svc.id.goog[${NAMESPACE}/${KSA_NAME}]" \
${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

printf "\nConnecting ksa with Service Account ...\n"
kubectl annotate serviceaccount \
--overwrite \
--namespace ${NAMESPACE} \
${KSA_NAME} \
iam.gke.io/gcp-service-account=${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com