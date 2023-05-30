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

# Link to the cluster.
export CLUSTER_NAME=main-cluster
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION --project $PROJECT_ID

# Set port-forwarding
python3 e2e/utils/port_forward.py --namespace default
sleep 3

# Run test.
PYTHONPATH=common/src python3 -m pytest --tb=no --disable-warnings e2e/gke_api_tests/

# Remove port-forwarding process.
# Alternative: list port-forward process: ps -ef | grep 'kubectl port-forward service/user-service'
pkill -f 'kubectl port-forward service/'
