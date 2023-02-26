# Google Cloud Solutions Template

**A template to generate a new project with built-in structure and features to accelerate your project setup.**

## TL;DR

Solutions Template is a boilerplate template for building repeatable
solutions with the best practices in architecture on Google Cloud, including GKE
clusters, Cloud Run, Test Automation, CI/CD, as well as development process.

This template provides built-in and ready-to-ship sample features including:
* Container-based microservices, can be deployed to a Kubernetes cluster or Cloud Run.
* Simplified deployment using Skaffold and Kustomize ([Blog](https://cloud.google.com/blog/topics/developers-practitioners/simplify-your-devops-using-skaffold)).
* Google Cloud foundation automation using [Terraform](https://www.terraform.io/).
* Automatically generated API documentation (via [FastAPI](https://fastapi.tiangolo.com/)).
* CI/CD deployment (with Github Actions).
* Cloud Run templates.

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

| Tool  | Required Version | Documentation site |
|---|---------------|---|
| gcloud CLI          | Latest        | https://cloud.google.com/sdk/docs/install |
| Terraform           | &gt;= v1.3.7  | https://developer.hashicorp.com/terraform/downloads |
| Skaffold (for GKE)  | &gt;= v2.1.0  | https://skaffold.dev/ |
| Kustomize (for GKE) | &gt;= v4.3.1  | https://kustomize.io/ |
| Cookiecutter        | &gt;= v2.1.1  | https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter |

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

Install **skaffold** and **kustomize**:

- For Google CloudShell or Linux/Ubuntu:
  ```
  curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/LATEST/skaffold-linux-amd64 && \
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

### Other dependencies (Optional)
- Apple M1 Chip Support for Terraform

If you are running commands on an Apple M1 chip Macbook, make sure run the following to add M1 support for Terraform:
```
brew install kreuzwerker/taps/m1-terraform-provider-helper
m1-terraform-provider-helper activate
m1-terraform-provider-helper install hashicorp/template -v v2.2.0
```

## Getting Started - Creating Solution Skeleton

### Create a new Google Cloud project (Optional):

> It is recommended to start with a brand new Google Cloud project to have a clean start.

Run the following to create a new Google Cloud project, or you can log in to Google Cloud Console to [create a new project](https://console.cloud.google.com/projectcreate).
```
export PROJECT_ID=<my-project-id>
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud auth application-default login # for Terraform to able to run gcloud with correct config.
gcloud auth application-default set-quota-project $PROJECT_ID
```

### Create skeleton code in a new folder with Cookiecutter

Run the following to generate skeleton code in a new folder:
```
cookiecutter https://github.com/GoogleCloudPlatform/solutions-template.git
```

Provide the required variables to Cookiecutter prompt, e.g.:
```
project_id: my-project-id
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

Once `cookiecutter` completes, you will see `<my-project-id>` folder created in
the path where you ran `cookiecutter` command.

### File structure

In the newly created folder, you will see the file structure like below:
```
<my-project-id>/
│   README.md
│   skaffold.yaml
├── docs
├── e2e
├── microservices
│   └── sample_service
│       ├── Dockerfile
│       ├── cloudbuild.yaml
│       ├── kustomize
│       ├── requirements.txt
│       ├── skaffold.yaml
│       ├── src
│       └   ...
│
└── common/
│   └── src/
│   │   Dockerfile
│   │   requirements.txt
│   │   skaffold.yaml
│   │   ...
│
└── .github/
```


## Setting up Google Cloud Project

```
# Set up environmental variables
export PROJECT_ID=<my-project-id>
export ADMIN_EMAIL=<my-email>
export REGION=us-central1
export API_DOMAIN=localhost

cd <my-project-id>
export BASE_DIR=$(pwd)
```

Log in to Google Cloud.
```
# Login to Google Cloud (if not on Cloud Shell)
gcloud auth login
gcloud config set project $PROJECT_ID
```

Run setup_all.sh to run all steps:
```
# Choose the microservice deployment options:
# "gke": to deploy services to GKE
# "cloudrun": to deploy services to Cloud Run
# "gke|cloudrun": to deploy services to both GKE and Cloud Run
export TEMPLATE_FEATURES="gke"

# Run all setup steps.
bash setup/setup_all.sh
```

Once microservice deployed successfully, you will see the message below:
```
The API endpoints are ready. See the auto-generated API docs at this URL: https://<your-sample-domain>/sample_service/docs
```

## Additional Documentations

You can find more documentations in [docs](docs) folder. In a nutshell, it covers the following:
- [INSTALLATION.md](docs/INSTALLATION.md) - The overall installation guide.
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide and code submission process.
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Development guide and code submission process.

In the [docs/components](docs/components/) folder, it contains a few more guidance based on each component/feature available in this template.
- [gke.md](gke.md) covers the overall developmeng guidance on Google Kubernetes Engine.
- [cloudrun.md](cloudrun.md) covers the guidance if you want to deploy microservice to Cloud Run.

## FAQ
- Who are the target audience/users for this Solutions template?
  - A: Any engineering team to start a new solution development project.

- Can I choose to deploy microservice just to Cloud Run?
  - A: Yes, please refer to [Setting up Google Cloud Project](README.md#setting-up-google-cloud-project) in this README.md to choose where to deploy microservices. Or you can refer to [INSTALLATION.md](docs/INSTALLATION.md) for more details.

- Can I use this template for non-Google or multi-Cloud environments?
  - A: We design this Solutions Template to work 100% out of the box with Google Cloud products. However you could customize the solution to meet your needs on multi-Cloud environment. See [Why Google Cloud](https://cloud.google.com/why-google-cloud) for details.

## Troubleshoot

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for details.
