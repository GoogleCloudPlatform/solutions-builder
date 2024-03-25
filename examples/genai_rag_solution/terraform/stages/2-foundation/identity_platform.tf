/**
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

# add timer to avoid errors on API enablement
resource "time_sleep" "wait_60_seconds" {
  depends_on      = [module.project_services]
  create_duration = "60s"
}

resource "google_apikeys_key" "idp_api_key" {
  depends_on   = [time_sleep.wait_60_seconds]
  name         = "idp-api-key"
  display_name = "API Key for Identity Platform"

  restrictions {
    api_targets {
      service = "identitytoolkit.googleapis.com"
    }
  }
}
