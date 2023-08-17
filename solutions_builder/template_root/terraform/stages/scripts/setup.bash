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

# Copy bootstrap and foundation terraform states to tfstate-bucket
gsutil cp ../1-bootstrap/terraform.tfstate gs://"${PROJECT_ID}"-tfstate/env/bootstrap/terraform.tfstate
gsutil cp ../12-foundation/terraform.tfstate gs://"${PROJECT_ID}"-tfstate/env/foundation/terraform.tfstate

# Enable deletion protection for the jump host
gcloud compute instances update jump-host --deletion-protection --project="${PROJECT_ID}"

# SCP github directory to jump host
TEMPLATE_ROOT=$(cd ../../.. && pwd)
gcloud compute scp "${TEMPLATE_ROOT}" jump-host:~ --zone="${ZONE}" --tunnel-through-iap --project="${PROJECT_ID}"

# Log onto the jump host using IAP and start tmux
gcloud compute ssh jump-host --zone="${ZONE}" --tunnel-through-iap --project="${PROJECT_ID}"
