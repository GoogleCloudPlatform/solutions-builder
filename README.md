# Google Cloud Solutions Template

> A template to generate a new project with built-in structure and features
> to accelerate your project setup.

## TL;DR

Solutions Template is a boilerplate template for building repeatable
solutions with the best practices in architecture on Google Cloud, including GKE
clusters, Cloud Run, Test Automation, CI/CD, as well as development process.

This template provides built-in and ready-to-ship sample features including:
* Container-based microservices, can be deployed to a Kubernetes cluster or Cloud Run.
* Simplified deployment using Skaffold and Kustomize
* Google Cloud foundation setup using Terraform
* CI/CD deployment (with Github Actions)
* Cloud Run templates

## Roadmap

Please see [Feature Requests in the Github issue list](https://github.com/GoogleCloudPlatform/solutions-template/issues?q=is%3Aopen+is%3Aissue+label%3A%22feature+request%22).

## Prerequisites

### Understanding Google Cloud

We recommend the following resources to get familiar with Google Cloud and microservices.

- What is [Microservice Architecture](https://cloud.google.com/learn/what-is-microservices-architecture)
- Kubernetes:
  - Learn about the [basics of Kubernetes](https://kubernetes.io/docs/concepts/overview/)
  - [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview) overview
  - [Skaffold](https://skaffold.dev/docs/), a command line tool that facilitates continuous development for container based & Kubernetes applications:
- Cloud Run:
  - Serverless container deployment and execution with [Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run)

### Tool requirements:

| Tool  | Required Version  | Documentation site |
|---|---|---|
| gcloud CLI          | Latest     | https://cloud.google.com/sdk/docs/install |
| Terraform           | >= v1.3.7  | https://developer.hashicorp.com/terraform/downloads |
| Skaffold (for GKE)  | >= v2.0.4  | https://skaffold.dev/ |
| Kustomize (for GKE) | >= v4.3.1  | https://kustomize.io/ |
| Cookiecutter        | >=2.1.1    | https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter |

### Install Cookiecutter ([Github](https://github.com/cookiecutter/cookiecutter)):
- For Google CloudShell or Linux/Ubuntu:
  ```
  python3 -m pip install --user cookiecutter
  ```
- For MacOS:
  ```
  brew install cookiecutter
  ```
- For Windows, refer this [installation guide](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter)

### Required packages for deploying to GKE cluster:
> You can skip this section if you choose to deploy microservices to Cloud Run only.

Install **skaffold (2.0.4 or later)** and kustomize:

- For Google CloudShell or Linux/Ubuntu:
  ```
  export SKAFFOLD_VERSION=v2.0.4
  curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/$SKAFFOLD_VERSION/skaffold-linux-amd64 && \
  sudo install skaffold /usr/local/bin/
  ```
- For MacOS:
  ```
  brew install skaffold kustomize
  ```
- For Windows:
  ```
  choco install -y skaffold kustomize gcloudsdk
  ```

### Apple M1 Chip Support for Terraform (Optional)

If you are running commands on an Apple M1 chip Macbook, make sure run the following to add M1 support for Terraform:
```
brew install kreuzwerker/taps/m1-terraform-provider-helper
m1-terraform-provider-helper activate
m1-terraform-provider-helper install hashicorp/template -v v2.2.0
```

## Getting Started - Creating Solution Skeleton

### Create a new Google Cloud project (Optional):

> It is recommeneded to start with a brand new Google Cloud project to have a clean start.

Run the following to create a new Google Cloud project, or you can log in to Google Cloud Console to [create a new project](https://console.cloud.google.com/projectcreate).
```
export PROJECT_ID=<my-project-folder>
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID
```

### Create skeleton code in a new folder with Cookiecutter

Run the following to generate skeleton code in a new folder:
```
cookiecutter https://github.com/GoogleCloudPlatform/solutions-template.git
```

Provide the required variables to Cookiecutter prompt, e.g.:
```
project_id: my-project-folder
project_name [My Awesome Project]:
project_short_description [My Awesome Project]:
project_slug [my_project]:
Google Cloud_region [us-central1]:
version [0.1.0]:
admin_email [admin@example.com]:
```
- The `project_id` is your Google Cloud project ID.
- You may leave variables as blank if you'd like to use the default value (except projdct_id).
- Notes: If you run into any issues with `cookiecutter`, please add `--verbose` at
the end of the command to show detailed errors.

Once `cookiecutter` completes, you will see the folder `<project_id>` created in
the path where you ran `cookiecutter` command.

### File structure

In the newly created folder, you will see the file structure like below:
```
<project_id>/
│   README.md
|   DEVELOPMENT.md
│   skaffold.yaml
│
└───microservices/
│   └───sample_service/
│       └───kustomize/
│       └───src/
│       │   Dockerfile
│       │   requirements.txt
│       │   skaffold.yaml
│       │   ...
│
└───common/
│   └───src/
│   │   Dockerfile
│   │   requirements.txt
│   │   skaffold.yaml
│   │   ...
│
└───.github/

```

- **README.md** - General info and setup guide.
- **DEVELOPMENT.md** - Development best practices, code submission flow, and other guidances.
- **skaffold.yaml** - The master Skaffold YAML file that defines how everything is built and deployed, depending on different profiles.
- **microservices** - The main directory for all microservices, can be broken down into individual folder for each microservie, e.g. `sample_service`.
  - [**microservice subfolder**] - Each microservice folder is a Docker container with [Skaffold](https://skaffold.dev/) + [Kustomize](https://kustomize.io/) to build images in different environments.
- **common** - The common image contains shared data models and util libraries used by all other microservices.
- **.github** - Github workflows including tests and CI/CD.

## Setting up Google Cloud Project

> (Optional) Check out the README.md in **my-project-folder** to check out the manual setup steps.

```
# Set up environmental variables
cd <my-project-folder>
export PROJECT_ID=<my-project-folder>
export API_DOMAIN=localhost
export BASE_DIR=$(pwd)
```

Log in to Google Cloud.
```
# Login to Google Cloud (if not on Cloud Shell)
gcloud auth login
gcloud auth application-default login
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID
```

Run setup_all.sh to run all steps:
```
# Choose the microservice deployment option: "gke" or "cloudrun"
export TEMPLATE_FEATURES="gke"

# Run all setup steps.
sh setup/setup_all.sh
```

It will then run the following steps:
- Updating GCP Organizational policies and required IAM roles.
- Run terraform to set up foundation and GKE cluster.
- Build and deploy microservices to GKE cluster.
- Test API endpoints (pytest).

Once microservice deployed successfully, you will see the message below:
```
The API endpoints are ready. See the auto-generated API docs at this URL: https://<your-sample-domain>/sample_service/docs
```

### Cleaning up all deployment and resources

Run the following to destory all deployment and resources.
> Note: there are some GCP resoureces that are not deletable, e.g. Firebase initialization.

```
cd $BASE_DIR/terraform/stages/gke
terraform destroy -auto-approve

cd $BASE_DIR/terraform/stages/cloudrun
terraform destroy -auto-approve

cd $BASE_DIR/terraform/stages/foundation
terraform destroy -auto-approve
```

## FAQ
- Who are the target audience/users for this Solutions template?
  - A: Any engineering team to start a new solution development project.
- Can I choose to deploy microservice just to Cloud Run?
  - A: Yes, please refer to `Getting Started - Setting up with setup_all script` in the README.md to choose where to deploy microservices.

## Troubleshoots

- I use a Apple M1 Mac and got errors like below when I ran `terraform init`:
  ```
  │ Error: Incompatible provider version
  │
  │ Provider registry.terraform.io/hashicorp/template v2.2.0 does not have a package available for your current platform,
  │ darwin_arm64.
  │
  │ Provider releases are separate from Terraform CLI releases, so not all providers are available for all platforms. Other
  │ versions of this provider may have different platforms supported.
  ```
  - A: Run the following to add support of M1 chip ([reference](https://kreuzwerker.de/en/post/use-m1-terraform-provider-helper-to-compile-terraform-providers-for-mac-m1))
    ```
    brew install kreuzwerker/taps/m1-terraform-provider-helper
    m1-terraform-provider-helper activate
    m1-terraform-provider-helper install hashicorp/template -v v2.2.0
    ```