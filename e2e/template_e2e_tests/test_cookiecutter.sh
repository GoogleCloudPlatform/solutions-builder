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

export OUTPUT_FOLDER=".test_output"

install_dependencies() {
  # Install Cookiecutter
  python3 -m pip install cookiecutter
}

build_template() {
  # Re-build template
  echo yes | bash ./build_tools/build_template.sh
}

# Create a new Google Cloud project
generate_new_project_id() {
  export PROJECT_ID=solutemp-e2e-$(uuidgen | head -c 8 | awk '{print tolower($0)}')
}

setup_working_folder() {
  mkdir -p $OUTPUT_FOLDER
  
  # Create skeleton code in a new folder with Cookiecutter
  cookiecutter . --overwrite-if-exists --no-input -o $OUTPUT_FOLDER project_id=$PROJECT_ID admin_email=$ADMIN_EMAIL
}

install_dependencies
build_template
if [[ "$PROJECT_ID" == 0 ]]; then
  generate_new_project_id
fi
setup_working_folder

echo "New project folder generated at $OUTPUT_FOLDER/$PROJECT_ID"
echo
