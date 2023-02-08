# Development
<!-- vscode-markdown-toc -->
* 1. [Project Requirements](#ProjectRequirements)
	* 1.1. [Tool requirements:](#Toolrequirements:)
* 2. [Code Submission Process](#CodeSubmissionProcess)
	* 2.1. [For the first-time setup:](#Forthefirst-timesetup:)
	* 2.2. [When making code changes](#Whenmakingcodechanges)
	* 2.3. [(For Repo Admins) Reviewing a Pull Request](#ForRepoAdminsReviewingaPullRequest)
* 3. [Local IDE Development (VS Code)](#LocalIDEDevelopmentVSCode)
	* 3.1. ["Common" container setup](#Commoncontainersetup)
	* 3.2. [Developing just "Common" container (VSCode)](#DevelopingjustCommoncontainerVSCode)
	* 3.3. [Microservice container setup](#Microservicecontainersetup)
	* 3.4. [Other IDE Setup](#OtherIDESetup)
* 4. [Local Development (minikube)](#LocalDevelopmentminikube)
	* 4.1. [ADVANCED: Run on minikube with your GCP credentials](#ADVANCED:RunonminikubewithyourGCPcredentials)
* 5. [Development with Kubernetes (GKE)](#DevelopmentwithKubernetesGKE)
	* 5.1. [ Initial setup for GKE development](#InitialsetupforGKEdevelopment)
	* 5.2. [Build and run all microservices in the default GKE cluster with live reload](#BuildandrunallmicroservicesinthedefaultGKEclusterwithlivereload)
	* 5.3. [Deploy to a specific GKE cluster](#DeploytoaspecificGKEcluster)
* 6. [Advanced Skaffold features (minikube or GKE)](#AdvancedSkaffoldfeaturesminikubeorGKE)
	* 6.1. [Build and run with specific microservice(s)](#Buildandrunwithspecificmicroservices)
	* 6.2. [Build and run microservices with a custom Source Repository path](#BuildandrunmicroserviceswithacustomSourceRepositorypath)
	* 6.3. [Build and run microservices with a different Skaffold profile](#BuildandrunmicroserviceswithadifferentSkaffoldprofile)
	* 6.4. [Skaffold profiles](#Skaffoldprofiles)
	* 6.5. [Switching from local (minikube) to GKE development](#SwitchingfromlocalminikubetoGKEdevelopment)
* 7. [Development with CloudRun (serverless)](#DevelopmentwithCloudRunserverless)
	* 7.1. [Mnaually Build and Deploy Microservices to CloudRun](#MnauallyBuildandDeployMicroservicestoCloudRun)
* 8. [Unit tests - microservices](#Unittests-microservices)
		* 8.1. [Run linter locally:](#Runlinterlocally:)
		* 8.2. [Unit test file format:](#Unittestfileformat:)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


This doc explains the development and code submission process.


##  1. <a name='ProjectRequirements'></a>Project Requirements

###  1.1. <a name='Toolrequirements:'></a>Tool requirements:

Install the following:

| Tool  | Required Version  | Documentation site |
|---|---|---|
| gcloud CLI          | Latest     | https://cloud.google.com/sdk/docs/install |
| Terraform           | >= v1.3.7  | https://developer.hashicorp.com/terraform/downloads |
| Skaffold (for GKE)  | >= v2.0.4  | https://skaffold.dev/ |
| Kustomize (for GKE) | >= v4.3.1  | https://kustomize.io/ |
| Cookiecutter        | >=2.1.1    | https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter |

Additonal useful tools:
* helm
* kubectx
* kubens

##  2. <a name='CodeSubmissionProcess'></a>Code Submission Process

###  2.1. <a name='Forthefirst-timesetup:'></a>For the first-time setup:
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


###  2.2. <a name='Whenmakingcodechanges'></a>When making code changes

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

###  2.3. <a name='ForRepoAdminsReviewingaPullRequest'></a>(For Repo Admins) Reviewing a Pull Request
For code reviewers, go to the Pull Requests page of the origin repo on Github.

* Go to the specific pull request, review and comment on the request.
branch.
* Alternatively, you can use Github CLI `gh` to check out a PR and run the codes locally: https://cli.github.com/manual/gh_pr_checkout
* If all goes well with tests passed, click Merge pull request to merge the changes to the master.

##  3. <a name='LocalIDEDevelopmentVSCode'></a>Local IDE Development (VS Code)

Here are settings and tips to set up your local IDE for development and testing of the code. These instructions are for VS Code.

As a shortcut, here is a sample `settings.json` for VS Code you will want to start with

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintPath": "pylint",
  "editor.formatOnSave": true,
  "python.formatting.provider": "yapf",
  "python.formatting.yapfArgs": [
    "--style={based_on_style: pep8, indent_width: 2}"
  ],
  "python.linting.pylintEnabled": true,
  "terminal.integrated.env.osx": {
    "PYTHONPATH": "${workspaceFolder}/common/src/"
  },
  "python.analysis.extraPaths": [
    "${workspaceFolder}/common/src/",
  ],
  "python.autoComplete.extraPaths": [
    "${workspaceFolder}/common/src/",
  ]
}
```

You may need to reload VS Code for these to take effect:
* CMD + SHIFT + P
* __Developer: Reload Window__

###  3.1. <a name='Commoncontainersetup'></a>"Common" container setup

The `common` container houses any common libraries, modules, data objects (ORM) etc that might be needed by other microservices. It can serve as the base container for builds in other microservices as shown in [this Dockerfile](./microservices/sample_service/Dockerfile#L1-L2)

Additional setup is required in a Python development environment so libraries added here are included in your IDE's code completion, etc.

###  3.2. <a name='DevelopingjustCommoncontainerVSCode'></a>Developing just "Common" container (VSCode)

* Set up VENV just for common

```
cd common

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

* Open Command Palette (CMD + SHIFT + P)
* Type "Python: Select Interpreter"
* Choose your new interpreter
  * will look something like `./common/.venv/bin/python3`

You should now be able to load modules and test them locally:

```
cd src
python
```

* In REPL:
```python
from common.models import User
user = User()
```

* Exit the VENV
```
deactivate
```

###  3.3. <a name='Microservicecontainersetup'></a>Microservice container setup

Any microservice containers that use common will follow the same setup, but will also require additional setup for your IDE's code-completion to register the common modules:

* Set up VENV just for microservice

Make sure you aren't in a VENV
```
deactivate
```

```
cd microservices/sample_service

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# install requirements from common!
pip install -r ../../common/requirements.txt

# install microservice requirements
pip install -r requirements.txt
```

* Open Command Palette (CMD + SHIFT + P)
* Type "Python: Select Interpreter"
* Choose your new interpreter
  * will look something like `./microservices/sample_service/.venv/bin/python3`

If you added the following to your VS Code `settings.json` file like mentiond before, the modules should load when you run from command line, and you should see code completion hints.

```json
{
  "terminal.integrated.env.osx": {
    "PYTHONPATH": "${workspaceFolder}/common/src/"
  },
  "python.analysis.extraPaths": [
    "${workspaceFolder}/common/src/"
  ]
}
```

You should now be able to load modules and test them locally:

```
cd microservices/sample_service/src

# run web server
python main.py
```

* Exit the VENV
```
deactivate
```

###  3.4. <a name='OtherIDESetup'></a>Other IDE Setup

* If VS Code asks you to install tools like `pylint`, etc. go ahead and do so.



##  4. <a name='LocalDevelopmentminikube'></a>Local Development (minikube)

Minikube can be used to provide an easy local Kuberentes environment for fast prototyping and debugging

* Install Minikube:

```
# For MacOS:
brew install minikube

# For Windows:
choco install -y minikube
```

* Simple local run

Make sure the Docker daemon is running locally. To start minikube:
```
# This will reset the kubectl context to the local minikube.
minikube start

# Build and run locally with hot reload:
skaffold dev
```

* Minikube run with ENV variables that are captured in Kustomize, for example [here](./microservices/sample_service/kustomize/base/env.properties)

```
# if PROJECT_ID variable is used in your containers
export PROJECT_ID=<your-project>

skaffold dev
```

###  4.1. <a name='ADVANCED:RunonminikubewithyourGCPcredentials'></a>ADVANCED: Run on minikube with your GCP credentials

This will mount your GCP credentials to every pod created in minikube. See [this guide](https://minikube.sigs.k8s.io/docs/handbook/addons/gcp-auth/) for more info.

The addon normally uses the [Google Application Default Credentials](https://google.aip.dev/auth/4110) as configured with `gcloud auth application-default login`. If you already have a json credentials file you want specify, such as to use a service account, set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to that file.

* User credentials

```
gcloud auth application-default login
minikube addons enable gcp-auth
```

* File based credentials

```
# Download a service accouunt credential file
export GOOGLE_APPLICATION_CREDENTIALS=<creds-path>.json
minikube addons enable gcp-auth
```


##  5. <a name='DevelopmentwithKubernetesGKE'></a>Development with Kubernetes (GKE)

###  5.1. <a name='InitialsetupforGKEdevelopment'></a> Initial setup for GKE development
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
* Run the following to setup the Kubernetes Service Account (ksa) in your namespace:
  ```
  export NAMESPACE=$SKAFFOLD_NAMESPACE
  ./setup/setup_ksa.sh
  ```

###  5.2. <a name='BuildandrunallmicroservicesinthedefaultGKEclusterwithlivereload'></a>Build and run all microservices in the default GKE cluster with live reload

> **_NOTE:_**  By default, skaffold builds with CloudBuild and runs in kubernetes cluster set in your local `kubeconfig`, using the namespace set above in `SKAFFOLD_NAMESPACE`. If it is set to your GKE cluster, it will deploy to the the cluster. If it's set to `minikube`, it will deploy there.
```
# check your current kubeconfig
kubectx

skaffold dev
```
- Please note that any change in the code locally will rerun the build process.

###  5.3. <a name='DeploytoaspecificGKEcluster'></a>Deploy to a specific GKE cluster

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

##  6. <a name='AdvancedSkaffoldfeaturesminikubeorGKE'></a>Advanced Skaffold features (minikube or GKE)

###  6.1. <a name='Buildandrunwithspecificmicroservices'></a>Build and run with specific microservice(s)

```
skaffold dev -m <service1>,<service2>
```

###  6.2. <a name='BuildandrunmicroserviceswithacustomSourceRepositorypath'></a>Build and run microservices with a custom Source Repository path
```
skaffold dev --default-repo=gcr.io/$PROJECT_ID
```


###  6.3. <a name='BuildandrunmicroserviceswithadifferentSkaffoldprofile'></a>Build and run microservices with a different Skaffold profile
```
# Using custom profile
skaffold dev -p custom

# Using prod profile
skaffold dev -p prod
```

###  6.4. <a name='Skaffoldprofiles'></a>Skaffold profiles

By default, the Skaffold YAML contains the following pre-defined profiles ready to use.

- **dev** - This is the default profile for local development, which will be activated automatically with the Kubectl context set to the default cluster of this GCP project.
- **prod** - This is the profile for building and deploying to the Prod environment, e.g. to a customer's Prod environment.
- **custom** - This is the profile for building and deploying to a custom GCP project environments, e.g. to deploy to a staging or a demo environment.

###  6.5. <a name='SwitchingfromlocalminikubetoGKEdevelopment'></a>Switching from local (minikube) to GKE development

Use the `kubectx` tool to change KubeConfig contexts, which are used by skaffold to target the appropriate cluster.

* Switching to minikube
```
# if minikube is already started
kubectx minikube

# if minikube is not started
# running this will also change the KubeConfig context
minikube start

skaffold dev
```

* Switching to GKE
```
# see available KubeContexts
kubectx

# choose your cluster
kubectx <YOUR_CLUSTER_NAMAE>

skaffold dev
```


##  7. <a name='DevelopmentwithCloudRunserverless'></a>Development with CloudRun (serverless)

###  7.1. <a name='MnauallyBuildandDeployMicroservicestoCloudRun'></a>Mnaually Build and Deploy Microservices to CloudRun

Build common image:
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

##  8. <a name='Unittests-microservices'></a>Unit tests - microservices

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

####  8.1. <a name='Runlinterlocally:'></a>Run linter locally:
```
python -m pylint $(git ls-files '*.py') --rcfile=$BASE_DIR/.pylintrc
```

####  8.2. <a name='Unittestfileformat:'></a>Unit test file format:

All unit test files follow the filename format:

- Python:
  ```
  <original_filename>_test.py