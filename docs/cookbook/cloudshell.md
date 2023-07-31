# Getting started a new Solution using Cloud Shell

## Create a new Solution

- Create a new GCP project
- Open up Cloud Shell
- Run the following in the Cloud Shell
  ```
  export PROJECT_ID=$DEVSHELL_PROJECT_ID
  sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
  ```

- Downgrade Kustomize to v4.5.7
  > Kustomize
  ```
  cd ~
  wget https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh
  sudo rm /usr/local/bin/kustomize
  sudo ./install_kustomize.sh 4.5.7 /usr/local/bin
  ```

- Ensure skaffold version to be &gt;= v2.2.0
  ```
  skaffold version
  # v2.2.0
  ```

- Generate skeleton code in a new folder:
  ```
  cookiecutter https://github.com/GoogleCloudPlatform/solutions-builder.git
  ```
  - Provide the required variables to Cookiecutter prompt.

- Build and deploy services to CloudRun:
  ```
  cd <my-project-id>

  # Choose the microservice deployment options: "gke", "cloudrun" or "gke|cloudrun"
  export TEMPLATE_FEATURES="cloudrun"
  source setup/init_env_var.sh
  bash setup/setup_all.sh
  ```
