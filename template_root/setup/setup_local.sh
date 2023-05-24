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

# Hardcoded the project ID for all local development.
declare -a EnvVars=(
  "PROJECT_ID"
  "SKAFFOLD_NAMESPACE"
  "REGION"
)

for variable in "${EnvVars[@]}"; do
  if [[ -z "${!variable}" ]]; then
    printf "%s is not set.\n" "$variable"
    exit 1
  fi
done

CLUSTER_NAME=main-cluster
EXPECTED_CONTEXT=gke_${PROJECT_ID}_${REGION}_${CLUSTER_NAME}

BLUE=$(tput setaf 4)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)
echo
echo "PROJECT_ID=${PROJECT_ID}"
echo "SKAFFOLD_NAMESPACE=${SKAFFOLD_NAMESPACE}"
echo "REGION=${REGION}"
echo

init() {
  printf "\n%sSwitch gcloud config to project %s %s\n" "${BLUE}" "${PROJECT_ID}" "${NORMAL}"
  EXISTING_PROJECT_ID=$(gcloud projects list --filter "${PROJECT_ID}" | grep "${PROJECT_ID}")
  if [[ "$EXISTING_PROJECT_ID" == "" ]]; then
    printf "Project %s doesn't exist or you don't have access.\n" "${PROJECT_ID}"
    printf "Terminated.\n"
    exit 0
  else
    printf "Project %s found.\n" "${PROJECT_ID}"
  fi
  
  gcloud config set project "$PROJECT_ID"
  
  printf "\n%sSet up gcloud and kubectl context ...%s\n" "${BLUE}" "${NORMAL}"
  gcloud container clusters get-credentials ${CLUSTER_NAME} --zone "${REGION}" --project "${PROJECT_ID}"
}

setup_namespace() {
  printf "\n%sCreating namespace: %s ...%s\n" "${BLUE}" "${SKAFFOLD_NAMESPACE}" "${NORMAL}"
  kubectl create ns "$SKAFFOLD_NAMESPACE"
  
  printf "\n%sUsing namespace %s for all kubectl operations ...%s\n" "${BLUE}" "${SKAFFOLD_NAMESPACE}" "${NORMAL}"
  kubectl config set-context --current --namespace="$SKAFFOLD_NAMESPACE"

  printf "\n%sVerifying the kubectl context name ...%s\n" "${BLUE}" "${NORMAL}"
  CURRENT_CONTEXT=$(kubectl config current-context)
  if [[ "$CURRENT_CONTEXT" == "$EXPECTED_CONTEXT" ]]; then
    printf "OK.\n"
  else
    printf "%sExpecting kubectl context as %s but got %s. %s\n" "${RED}" "${EXPECTED_CONTEXT}" "${CURRENT_CONTEXT}" "${NORMAL}"
  fi
}

read -p  "${BLUE}This will set up for local development using namespace \
\"${SKAFFOLD_NAMESPACE}\" in \"$CLUSTER_NAME\" in project \"$PROJECT_ID\". \
Continue? (y/n) ${NORMAL}" -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo
else
  printf "\nTerminated.\n"
  exit 0
fi

init
add_service_account_keys
setup_namespace

printf "\n%sDone. %s\n" "${BLUE}" "${NORMAL}"
