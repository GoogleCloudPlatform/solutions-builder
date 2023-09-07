"""
Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
  update = False

  def hook(self, context):
    module_version = context["module_version"]
    template_path = context["template_path"]
    subfolders = context["subfolders"] or []
    subfolders.sort(reverse=True)
    version_folder = subfolders[0]
    version_folder_path = f"{template_path}/{version_folder}"

    print(f"version_folder_path = {version_folder_path}")
    print(f"module_version = {module_version}")

    # Convert module_version
    if not module_version or module_version == "":
      version_folder = "."
    elif module_version.lower() == "latest":
      version_folder = subfolders[0]
    else:
      version_folder = module_version

    # Check if the module_version folder exists.
    if not os.path.isdir(version_folder_path):
      version_folder = "."

    print(f"Using version folder: {version_folder}")

    context["_subdirectory"] = version_folder

    print(context)
