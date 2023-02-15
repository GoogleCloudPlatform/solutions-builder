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

PROJECT_ID="solutions-template-e2etest"
REGION="us-central1"
ADMIN_EMAIL="your_email@example.com"
API_DOMAIN="localhost"

declare -a EnvVars=(
  "PROJECT_ID"
  "REGION"
  "ADMIN_EMAIL"
  "API_DOMAIN"
)

for variable in "${EnvVars[@]}"; do
  if [[ -z "${!variable}" ]]; then
    input_value=""
    while [[ -z "$input_value" ]]; do
      read -p "Enter the value for ${variable}: " input_value
      declare "${variable}=$input_value"
    done
  fi
done

# Full list of folders to copy.
declare -a folders_to_copy=(
  ".github"
  "common"
  "setup"
  # FIXME: The symblink doesn't work with cookiecutter. Need to find a
  # solution to reduce the duplication between root folder vs. cookiecutter.
  # See: https://github.com/cookiecutter/cookiecutter/issues/865
  "cicd"
  "docs"
  "e2e"
  "microservices"
  "terraform"
)

# List all files that will be skipped in the cookiecutter folder.
# FIXME: Use regex to match the list.
declare -a files_to_remove=(
  "cookiecutter.json"
  "CONTRIBUTING.md"
)

declare -a ignore_list=(
  "__pycache__"
  ".coverage"
  ".github/workflows/template_e2e_test.yaml"
  ".pytest_cache"
  ".terraform*"
  ".venv"
  ".vscode"
  "CONTRIBUTING.md"
  "cookiecutter.json"
  "e2e/template_e2e_tests"
  "microservices/frontend_angular/.angular"
  "microservices/frontend_angular/node_modules"
  "microservices/frontend_angular/dist"
)

# Currently avoid adding symlink in template folder. Once added the folder,
# please add to ./cookiecutter.json for reverse mapping.
declare -a symlink_folders=(
)

get_machine_type() {
  unameOut="$(uname -s)"
  case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
  esac
  echo "$machine"
}
MACHINE_TYPE=$(get_machine_type)
TEMPLATE_FOLDER_NAME='{{cookiecutter.project_id}}'

build_template() {
  build_folder=$1

  echo "Deleting the existing build folder ${build_folder}"
  rm -rf "${build_folder}"

  echo "Creating build folder at ${build_folder}"
  mkdir -p "$build_folder"
  cp {.,}* "$build_folder"
  cp build_tools/template_docs/*.md "$build_folder"

  echo "Replacing with cookiecutter vars with:"
  echo
  echo "project_id: ${PROJECT_ID} => {{cookiecutter.project_id}}"
  echo "gcp_region: ${REGION} => {{cookiecutter.gcp_region}}"
  echo "admin_email: ${ADMIN_EMAIL} => {{cookiecutter.admin_email}}"
  echo "api_domain: ${API_DOMAIN} => {{cookiecutter.api_domain}}"
  echo

  # Combine excluded files to params.
  exclude_str=""
  for item in "${ignore_list[@]}"
  do
    exclude_str=${exclude_str:+$exclude_str }--exclude="\"${item}\""
  done

  # Copy folders in the selected list.
  for folder in "${folders_to_copy[@]}"; do
    echo "Copying folder \"${folder}\"..."
    command="rsync -rv ${folder} ${build_folder}/ ${exclude_str}"
    eval $command

    echo
    echo "Replacing with cookiecutter vars in folder $build_folder/$folder"
    replace_cookiecutter_vars "$build_folder/$folder"
    echo
  done

  # Clean up backup files
  find . -name '.!*' -exec rm -rf {} \;

  # Remove skipped files based on the list.
  echo
  for filename in "${files_to_remove[@]}"; do
    echo "Removing $build_folder/$filename"
    rm -rf "$build_folder/$filename"
  done

  # Copy symlink folders
  for folder in "${symlink_folders[@]}"; do
    ln -s "../$folder" "$build_folder/$folder"
  done

  # Verify
  verify_result=""
  for folder in "${folders[@]}"; do
    verify_result+=$(verify "$build_folder/$folder")
  done

  if [ "$verify_result" != "" ]; then
    echo
    echo "The following file(s) still have keywords not replaced with cookiecutter vars."
    echo "$verify_result"
    echo
    exit 1
  fi
}

replace_cookiecutter_vars() {
  find_cmd="find $1 -type f \
    ! -path '*/node_modules/*' \
    ! -path '*/.terraform/*' \
    ! -path '*/.github/assets/*' \
    -name '*.py' -o \
    -name '*.js' -o \
    -name '*.ts' -o \
    -name '*.sh' -o \
    -name '*.yaml' -o \
    -name '*.yml' -o \
    -name '*.tf' -o \
    -name '*.cfg' -o \
    -name '*.txt' -o \
    -name '*.md' -o \
    -name 'Dockerfile' \
  "

  for fname in $(eval "$find_cmd"); do
    echo "$fname"
    if [ "${MACHINE_TYPE}" == "Mac" ]; then
      sed -i '' "s/${PROJECT_ID}/{{cookiecutter.project_id}}/g" "$fname"
      sed -i '' "s/${REGION}/{{cookiecutter.gcp_region}}/g" "$fname"
      sed -i '' "s/${ADMIN_EMAIL}/{{cookiecutter.admin_email}}/g" "$fname"
      sed -i '' "s/${API_DOMAIN}/{{cookiecutter.api_domain}}/g" "$fname"
    else
      sed -i "s/${PROJECT_ID}/{{cookiecutter.project_id}}/g" "$fname"
      sed -i "s/${REGION}/{{cookiecutter.gcp_region}}/g" "$fname"
      sed -i "s/${ADMIN_EMAIL}/{{cookiecutter.admin_email}}/g" "$fname"
      sed -i "s/${API_DOMAIN}/{{cookiecutter.api_domain}}/g" "$fname"
    fi
  done
}

verify() {
  grep -rnw "$1" -e "${PROJECT_ID}"
  grep -rnw "$1" -e "${REGION}"
  grep -rnw "$1" -e "${ADMIN_EMAIL}"
  grep -rnw "$1" -e "${API_DOMAIN}"
}

build_path=$1
if [ -z "${build_path}" ]; then
  build_path="."
fi
build_folder="${build_path}/$TEMPLATE_FOLDER_NAME"

echo
echo "This will build cookiecutter template at ${build_folder} (will override). Continue? (y/n)"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
  build_template $build_folder
  echo
  echo "Template Built Complete."
  echo
else
  echo "Aborted."
  echo
fi
