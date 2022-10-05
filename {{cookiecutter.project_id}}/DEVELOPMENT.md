# Development
<!-- vscode-markdown-toc -->
* 1. [Project Requirements](#ProjectRequirements)
* 2. [Code Submission Process](#CodeSubmissionProcess)
	* 2.1. [For the first-time setup:](#Forthefirst-timesetup:)
	* 2.2. [When making code changes](#Whenmakingcodechanges)
	* 2.3. [(For Repo Admins) Reviewing a Pull Request](#ForRepoAdminsReviewingaPullRequest)
* 3. [Local Development (minikube)](#LocalDevelopmentminikube)
	* 3.1. [ADVANCED: Run on minikube with your GCP credentials](#ADVANCED:RunonminikubewithyourGCPcredentials)
* 4. [Development with Kubernetes (GKE)](#DevelopmentwithKubernetesGKE)
	* 4.1. [ Initial setup for GKE development](#InitialsetupforGKEdevelopment)
	* 4.2. [Build and run all microservices in the default GKE cluster with live reload](#BuildandrunallmicroservicesinthedefaultGKEclusterwithlivereload)
	* 4.3. [Deploy to a specific GKE cluster](#DeploytoaspecificGKEcluster)
* 5. [Advanced Skaffold features (minikube or GKE)](#AdvancedSkaffoldfeaturesminikubeorGKE)
	* 5.1. [Build and run with specific microservice(s)](#Buildandrunwithspecificmicroservices)
	* 5.2. [Build and run microservices with a custom Source Repository path](#BuildandrunmicroserviceswithacustomSourceRepositorypath)
	* 5.3. [Build and run microservices with a different Skaffold profile](#BuildandrunmicroserviceswithadifferentSkaffoldprofile)
	* 5.4. [Skaffold profiles](#Skaffoldprofiles)
	* 5.5. [Switching from local (minikube) to GKE development](#SwitchingfromlocalminikubetoGKEdevelopment)
* 6. [Development with CloudRun (serverless)](#DevelopmentwithCloudRunserverless)
* 7. [Unit tests - microservices](#Unittests-microservices)
		* 7.1. [Run linter locally:](#Runlinterlocally:)
		* 7.2. [Unit test file format:](#Unittestfileformat:)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


This doc explains the development workflow so you can get started contributing code to {{cookiecutter.project_name}}

##  1. <a name='ProjectRequirements'></a>Project Requirements

Install the following based on [the versions for this project](./README.md#ProjectRequirements)
* skaffold
* kustomize
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

##  3. <a name='LocalDevelopmentminikube'></a>Local Development (minikube)

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

* Minikube run with ENV variables

```
# if PROJECT_ID variable is used in your containers
export PROJECT_ID=<your-project>

skaffold dev
```

###  3.1. <a name='ADVANCED:RunonminikubewithyourGCPcredentials'></a>ADVANCED: Run on minikube with your GCP credentials

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


##  4. <a name='DevelopmentwithKubernetesGKE'></a>Development with Kubernetes (GKE)

###  4.1. <a name='InitialsetupforGKEdevelopment'></a> Initial setup for GKE development
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

###  4.2. <a name='BuildandrunallmicroservicesinthedefaultGKEclusterwithlivereload'></a>Build and run all microservices in the default GKE cluster with live reload

> **_NOTE:_**  By default, skaffold builds with CloudBuild and runs in GKE cluster, using the namespace set above.
```
skaffold dev
```
- Please note that any change in the code locally will rerun the build process.

###  4.3. <a name='DeploytoaspecificGKEcluster'></a>Deploy to a specific GKE cluster

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

##  5. <a name='AdvancedSkaffoldfeaturesminikubeorGKE'></a>Advanced Skaffold features (minikube or GKE)

###  5.1. <a name='Buildandrunwithspecificmicroservices'></a>Build and run with specific microservice(s)

```
skaffold dev -m <service1>,<service2>
```

###  5.2. <a name='BuildandrunmicroserviceswithacustomSourceRepositorypath'></a>Build and run microservices with a custom Source Repository path
```
skaffold dev --default-repo=gcr.io/$PROJECT_ID
```


###  5.3. <a name='BuildandrunmicroserviceswithadifferentSkaffoldprofile'></a>Build and run microservices with a different Skaffold profile
```
# Using custom profile
skaffold dev -p custom

# Using prod profile
skaffold dev -p prod
```

###  5.4. <a name='Skaffoldprofiles'></a>Skaffold profiles

By default, the Skaffold YAML contains the following pre-defined profiles ready to use.

- **dev** - This is the default profile for local development, which will be activated automatically with the Kubectl context set to the default cluster of this GCP project.
- **prod** - This is the profile for building and deploying to the Prod environment, e.g. to a customer's Prod environment.
- **custom** - This is the profile for building and deploying to a custom GCP project environments, e.g. to deploy to a staging or a demo environment.

###  5.5. <a name='SwitchingfromlocalminikubetoGKEdevelopment'></a>Switching from local (minikube) to GKE development

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



##  6. <a name='DevelopmentwithCloudRunserverless'></a>Development with CloudRun (serverless)

TBD

##  7. <a name='Unittests-microservices'></a>Unit tests - microservices

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

####  7.1. <a name='Runlinterlocally:'></a>Run linter locally:
```
python -m pylint $(git ls-files '*.py') --rcfile=$BASE_DIR/.pylintrc
```

####  7.2. <a name='Unittestfileformat:'></a>Unit test file format:

All unit test files follow the filename format:

- Python:
  ```
  <original_filename>_test.py