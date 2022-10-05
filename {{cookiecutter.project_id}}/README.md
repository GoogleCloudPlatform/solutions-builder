# {{cookiecutter.project_name}}

> This solution skeleton is created from https://github.com/GoogleCloudPlatform/solutions-template

Please contact {{cookiecutter.admin_email}} for any questions.

# Getting Started

### Prerequisites

```
# Set up environmental variables
export PROJECT_ID={{cookiecutter.project_id}}
export ADMIN_EMAIL={{cookiecutter.admin_email}}
export REGION={{cookiecutter.gcp_region}}
export API_DOMAIN={{cookiecutter.api_domain}}
export BASE_DIR=$(pwd)

# Login to Google Cloud
gcloud auth application-default login
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID
```

For development with Kubernetes on GKE:

Install required packages:

- For MacOS:
  ```
  brew install --cask skaffold kustomize google-cloud-sdk
  ```

- For Windows:
  ```
  choco install -y skaffold kustomize gcloudsdk
  ```

- For Linux/Ubuntu:
  ```
  curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
  sudo install skaffold /usr/local/bin/
  ```

* Make sure to use __skaffold 1.24.1__ or later for development.

### GCP Orgnization policy

Optionally, you may need to update Organization policies for CI/CD test automation.

Run the following commands to update Organization policies:
```
export ORGANIZATION_ID=$(gcloud organizations list --format="value(name)")
gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
```

Or, change the following Organization policy constraints in [GCP Console](https://console.cloud.google.com/iam-admin/orgpolicies)
- constraints/compute.requireOsLogin - Enforced Off
- constraints/compute.vmExternalIpAccess - Allow All

### GCP Foundation Setup - Terraform

Set up Terraform environment variables and GCS bucket for state file.
If the new project is just created recently, you may need to wait for 1-2 minutes
before running the Terraform command.

```
export TF_VAR_project_id=$PROJECT_ID
export TF_VAR_api_domain=$API_DOMAIN
export TF_VAR_web_app_domain=$API_DOMAIN
export TF_VAR_admin_email=$ADMIN_EMAIL
export TF_BUCKET_NAME="${PROJECT_ID}-tfstate"
export TF_BUCKET_LOCATION="us"

# Grant Storage admin to the current user IAM.
export CURRENT_USER=$(gcloud config list account --format "value(core.account)")
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$CURRENT_USER" --role='roles/storage.admin'

# Create Terraform Statefile in GCS bucket.
bash setup/setup_terraform.sh
```

Run Terraform apply

```
cd terraform/environments/dev
terraform init -backend-config=bucket=$TF_BUCKET_NAME

# Enabling GCP services first.
terraform apply -target=module.project_services -target=module.service_accounts -auto-approve

# Run the rest of Terraform
terraform apply -auto-approve
```

### Deploying Kubernetes Microservices to GKE

Connect to the `default-cluster`:
```
gcloud container clusters get-credentials main-cluster --region $REGION --project $PROJECT_ID
```

Build all microservices (including web app) and deploy to the cluster:
```
cd $BASE_DIR
skaffold run -p prod --default-repo=gcr.io/$PROJECT_ID
```

Test with API endpoint:
```
export API_DOMAIN=$(kubectl describe ingress | grep Address | awk '{print $2}')
echo "http://${API_DOMAIN}/sample_service/docs"
```

### Deploying Microservices to CloudRun

Build common image
```
cd common
gcloud builds submit --config=cloudbuild.yaml --substitutions=\
_PROJECT_ID="$PROJECT_ID",\
_REGION="$REGION",\
_REPOSITORY="cloudrun",\
_IMAGE="common"
```

Set up endpoint permission:
```
export SERVICE_NAME=sample-service
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

Build service image
```
gcloud builds submit --config=cloudbuild.yaml --substitutions=\
_CLOUD_RUN_SERVICE_NAME=$SERVICE_NAME,\
_PROJECT_ID="$PROJECT_ID",\
_REGION="$REGION",\
_REPOSITORY="cloudrun",\
_IMAGE="cloudrun-sample",\
_SERVICE_ACCOUNT="deployment-dev@$PROJECT_ID.iam.gserviceaccount.com",\
_ALLOW_UNAUTHENTICATED_FLAG="--allow-unauthenticated"
```

Manually deploy a microservice to CloudRun with public endpoint:
```
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

# Development

## Development with Kubernetes

### Initial setup for local development
After cloning the repo, please set up for local development.

* Export GCP project id and the namespace based on your Github handle (i.e. user ID)
  ```
  export PROJECT_ID={{cookiecutter.project_id}}
  export REGION={{cookiecutter.gcp_region}}
  export SKAFFOLD_NAMESPACE=<Replace with your Github user ID>
  ```
* Run the following to create skaffold namespace, and use the default cluster name as `default_cluster`:
  ```
  ./setup/setup_local.sh
  ```

## Build and Run

### Build and run all microservices in the default GKE cluster with live reload

> **_NOTE:_**  By default, skaffold builds with CloudBuild and runs in GKE cluster, using the namespace set above.
```
skaffold dev
```
- Please note that any change in the code locally will rerun the build process.

### Build and run with specific microservice(s)

```
skaffold dev -m <service1>,<service2>
```

### Build and run microservices with a custom Source Repository path
```
skaffold dev --default-repo=gcr.io/$PROJECT_ID
```

### Run with local minikube cluster

#### Install Minikube:

```
# For MacOS:
brew install minikube

# For Windows:
choco install -y minikube
```

#### Simple local run

Make sure the Docker daemon is running locally. To start minikube:
```
# This will reset the kubectl context to the local minikube.
minikube start

# Build and run locally with hot reload:
skaffold dev
```

#### Minikube run with ENV variables

```
# if PROJECT_ID variable is used in your containers
export PROJECT_ID=<your-project>

skaffold dev
```

#### ADVANCED: Run on minikube with your GCP credentials

This will mount your GCP credentials to every pod created in minikube. See [this guide](https://minikube.sigs.k8s.io/docs/handbook/addons/gcp-auth/) for more info.

The addon normally uses the [Google Application Default Credentials](https://google.aip.dev/auth/4110) as configured with `gcloud auth application-default login`. If you already have a json credentials file you want specify, such as to use a service account, set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to that file.

##### User credentials

```
gcloud auth application-default login
minikube addons enable gcp-auth
```

##### File based credentials

```
# Download a service accouunt credential file
export GOOGLE_APPLICATION_CREDENTIALS=<creds-path>.json
minikube addons enable gcp-auth
```

### Deploy to a specific GKE cluster

> **IMPORTANT**: Please change gcloud project and kubectl context before running skaffold.

```
export PROJECT_ID={{cookiecutter.project_id}}

# Switch to a specific project.
gcloud config set project $PROJECT_ID

# Assuming the default cluster name is "default_cluster".
gcloud container clusters get-credentials default_cluster --zone {{cookiecutter.gcp_region}}-a --project $PROJECT_ID
```

Run with skaffold:
```
skaffold run -p custom --default-repo=gcr.io/$PROJECT_ID

# Or run with hot reload and live logs:
skaffold dev -p custom --default-repo=gcr.io/$PROJECT_ID
```

### Build and run microservices with a different Skaffold profile
```
# Using custom profile
skaffold dev -p custom

# Using prod profile
skaffold dev -p prod
```

### Skaffold profiles

By default, the Skaffold YAML contains the following pre-defined profiles ready to use.

- **dev** - This is the default profile for local development, which will be activated automatically with the Kubectl context set to the default cluster of this GCP project.
- **prod** - This is the profile for building and deploying to the Prod environment, e.g. to a customer's Prod environment.
- **custom** - This is the profile for building and deploying to a custom GCP project environments, e.g. to deploy to a staging or a demo environment.

## Development with CloudRun (serverless)

TBD

## Unit tests - microservices

Install Firebase CLI:
```
curl -sL https://firebase.tools | bash
```

Install Virtualenv and pip requirements
```
# Go to a specific microservie folder:
export BASE_DIR=$(pwd)
cd microservices/sample_service
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
```

Run unit tests locally:
```
PYTEST_ADDOPTS="--cache-clear --cov . " PYTHONPATH=$BASE_DIR/common/src python -m pytest
```

#### Run linter locally:
```
python -m pylint $(git ls-files '*.py') --rcfile=$BASE_DIR/.pylintrc
```

#### Unit test file format:

All unit test files follow the filename format:

- Python:
  ```
  <original_filename>_test.py
  ```

## End-to-End API tests

TBD

# CI/CD and Test Automation

## Github Actions

### Test Github Action workflows locally

- Install Docker desktop: https://www.docker.com/products/docker-desktop/
- Install [Act](https://github.com/nektos/act)
  ```
  # Mac
  brew install act

  # Windows
  choco install act-cli
  ```

- Run a specific Workflow
  ```
  act --workflows .github/workflows/e2e_gke_api_test.yaml
  ```

## CloudBuild

TBD

# Development Process & Best Practices

## Code Submission Process

### For the first-time setup:
* Create a fork of a Git repository
  - Go to the specific Git repository’s page, click Fork at the right corner of the page:
* Choose your own Github profile to create this fork under your name.
* Clone the repo to your local computer. (Replace the variables accordingly)
  ```
  cd ~/workspace
  git clone git@github.com:$YOUR_GITHUB_ID/$REPOSITORY_NAME.git
  cd $REPOSITORY_NAME
  ```
  - If you encounter permission-related errors while cloning the repo, follow [this guide](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to create and add an SSH key for Github access (especially when checking out code with git@github.com URLs)
* Verify if the local git copy has the right remote endpoint.
  ```
  git remote -v
  # This will display the detailed remote list like below.
  # origin  git@github.com:<your-github-id>/$REPOSITORY_NAME.git (fetch)
  # origin  git@github.com:<your-github-id>/$REPOSITORY_NAME.git (push)
  ```

  - If for some reason your local git copy doesn’t have the correct remotes, run the following:
    ```
    git remote add origin git@github.com:$YOUR_GITHUB_ID/$REPOSITORY_NAME.git
    # or to reset the URL if origin remote exists
    git remote set-url origin git@github.com:$YOUR_GITHUB_ID/$REPOSITORY_NAME.git
    ```

* Add the upstream repo to the remote list as **upstream**.
  ```
  git remote add upstream git@github.com:$UPSTREAM_REPOSITORY_NAME.git
  ```
  - In default case, the $UPSTREAM_REPOSITORY_NAME will be the repo that you make the fork from.


### When making code changes

* Sync your fork with the latest commits in upstream/master branch. (more info)
  ```
  # In your local fork repo folder.
  git checkout -f master
  git pull upstream master
  ```

* Create a new local branch to start a new task (e.g. working on a feature or a bug fix):
  ```
  # This will create a new branch.
  git checkout -b feature_xyz
  ```

* After making changes, commit the local change to this custom branch and push to your fork repo on Github. Alternatively, you can use editors like VSCode to commit the changes easily.
  ```
  git commit -a -m 'Your description'
  git push
  # Or, if it doesn’t push to the origin remote by default.
  git push --set-upstream origin $YOUR_BRANCH_NAME
  ```
  - This will submit the changes to your fork repo on Github.

* Go to the your Github fork repo web page, click the “Compare & Pull Request” in the notification. In the Pull Request form, make sure that:
  - The upstream repo name is correct
  - The destination branch is set to master.
  - The source branch is your custom branch. (e.g. feature_xyz in the example above.)
  - Alternatively, you can pick specific reviewers for this pull request.

* Once the pull request is created, it will appear on the Pull Request list of the upstream origin repository, which will automatically run tests and checks via the CI/CD.

* If any tests failed, fix the codes in your local branch, re-commit and push the changes to the same custom branch.
  ```
  # after fixing the code…
  git commit -a -m 'another fix'
  git push
  ```
  - This will update the pull request and re-run all necessary tests automatically.
  - If all tests passed, you may wait for the reviewers’ approval.

* Once all tests pass and get approvals from reviewer(s), the reviewer or Repo Admin will merge the pull request back to the origin master branch.

### (For Repo Admins) Reviewing a Pull Request
For code reviewers, go to the Pull Requests page of the origin repo on Github.

* Go to the specific pull request, review and comment on the request.
branch.
* Alternatively, you can use Github CLI `gh` to check out a PR and run the codes locally: https://cli.github.com/manual/gh_pr_checkout
* If all goes well with tests passed, click Merge pull request to merge the changes to the master.
