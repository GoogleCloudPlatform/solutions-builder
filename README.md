# Google Cloud Solutions Template

> A template to generate a new project with built-in structure and features
> to accelerate your project setup.

## TL;DR

Solutions Template is a boilerplate template for building repeatable
solutions with the best practices in architecture on Google Cloud, including GKE
clusters, Test Automation, CI/CD, as well as development process.

This template provides built-in and ready-to-ship sample features including:
* Kubernetes-based microservices
* Simplified deployment using Skaffold and Kustomize
* Terraform Google Cloud foundation setup
* CI/CD deployment (with Github Actions)
* [In Progress] CI/CD deployment with CloudBuild
* [In Progress] CloudRun templates

## Getting Started

### Prerequisites

Install Cookiecutter ([Github](https://github.com/cookiecutter/cookiecutter)):
- For MacOS:
  ```
  brew install cookiecutter
  ```

- For Windows, refer this [installation guide](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter)

Install other required dependencies:

- For MacOS:
  ```
  brew install --cask skaffold kustomize google-cloud-sdk
  ```

- For Windows:
  ```
  choco install -y skaffold kustomize gcloudsdk
  ```

* Make sure to use __skaffold 1.39__ or later for development.

### Project Requirements

| Tool  | Current Version  |
|---|---|
| Skaffold  | v1.39.2  |
| GKE  | v1.22  |
| Kustomize  | v4.3.1  |

### Create a new project with Cookiecutter

Run the following to generate skeleton code in a new folder:
```
cookiecutter git@github.com:GoogleCloudPlatform/solutions-template.git
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
- You may leave variables as blank if you'd like to use the default value (except projdct_id).
- Notes: If you run into any issues with `cookiecutter`, please add `--verbose` at
the end of the command to show detailed errors.

Once `cookiecutter` completes, you will see the folder `<project_id>` created in
the path where you ran `cookiecutter` command.

### Inside the newly created folder

You will see the file structure like below:
```
<project_id>/
│   README.md
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
### File structure details

- **README.md** - This contains all details regarding the development and deployment.
- **skaffold.yaml** - This is the master Skaffold YAML file that defines how everything is built and deployed, depending on different profiles.
- **microservices** - The main directory for all microservices, can be broken down into individual folder for each microservie, e.g. `sample_service`.
  - [**microservice subfolder**] - Each microservice folder is a Docker container with [Skaffold](https://skaffold.dev/) + [Kustomize](https://kustomize.io/) to build images in different environments.
- **common** - The common image contains shared data models and util libraries used by all other microservices.

## Project Initialization

Once the new project folder is created, run the following [Terraform](https://www.terraform.io/) commands to set up your project in your project folder:

```
# Init gcloud command.
export PROJECT_ID=<my-project-id>
gcloud auth application-default login
gcloud config set project $PROJECT_ID

# Create Terraform State bucket.
export BUCKET_NAME=$PROJECT_ID-tfstate
export BUCKET_LOCATION=us
gsutil mb -l $BUCKET_LOCATION gs://$BUCKET_NAME
gsutil versioning set on gs://$BUCKET_NAME

cd terraform/environments/dev
terraform init
terraform apply
```

## Built-in Features

In a nutshell, Solutions Template offers the following built-in features with working sample code:
- A sample microservice with CRUD API endpoints on Kubernetes (GKE).
- A built-in Ingress supporting custom DNS domain.
- Test Automation and CI/CD with Github Action.

We are also working on the following features:
- CloudRun Services
- Test Automation and Ci/CD with CloudBuild

### Microservices on Kubernetes (GKE)

This Solutions Template contains a working stack of microservices on Kubernetes (GKE).
You will be able to deploy and run the `sample-service` with simple CRUD operations for `User` objects stored in Firestore.

It comes with ready-to-deploy structure using Skaffold and Kustomize. See examples below.

#### Run with all microservices

To deploy all microservices to the GKE cluster, simply run the following:

```
export PROJECT_ID=<your-project>
export SKAFFOLD_NAMESPACE=default

# Or if you'd like to run with a different kubernetes namespace:
export SKAFFOLD_NAMESPACE=<another_namespace>

# Deploy all microservices to the default GKE cluster:
skaffold dev

# Alternatively, you can run with a specific Skaffold profile and/or a custom image registry:
skaffold dev -p dev --default-repo=gcr.io/$PROJECT_ID
```

This will deploy a `sample-service` microservice to the default GKE cluster. Now you can:
- Open http://localhost:8888/sample_service/v1/docs in a browser window
- Verify if you see the Swagger API documentations

For more information about Kubernetes microservices development using Solutions Template, please refer to [this documentation]().


### CloudRun Services

TBD

### Test automation and CI/CD

TBD

## Roadmap

TBD

## FAQ

TBD
