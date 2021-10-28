# Google Public Sector Solutions Template

> This is the boilerplate template for building repeatable solutions with the \
> best practices in architecture on GCP, including GKE clusters, CI/CD, as \
> well as development process.

Please contact jonchen@google.com for any questions.

## Getting Started

### Prerequisites

Set up required environment variables
```
export PROJECT_ID={{cookiecutter.project_id}}
```

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

* Make sure to use __skaffold 1.24.1__ or later for development.

### Create new project with Cookiecutter

Run the following to generate a new project:
```
cookiecutter https://source.developers.google.com/p/psds-solutions-template/r/github_gps-solutions_solutions-template
```

Provide the required variables to Cookiecutter prompt, e.g.:
```
project_id: jonchen-test
project_name [Google GPS Solutions Template]:
project_short_description [Google GPS Solutions Template.]:
project_slug [jonchen_test]:
gcp_region [us-central1]:
version [0.1.0]:
admin_email [jonchen@google.com]:
```
- You can leave a particular variable as blank if you'd like to use the default value.

Notes: If you run into any issues with `cookiecutter`, please add `--verbose` at
the end of the command to show detailed errors.

### Inside the newly created folder

Once `cookiecutter` completes, you will see the folder `<project_id>` created in
the path where you ran `cookiecutter` command.

You will see the file structure like below:
```
<project_id>
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
#### Details of the file structure:

- **README.md** - This contains all details regarding the development and deployment.
- **skaffold.yaml** - This is the master Skaffold YAML file that defines how everything is built and deployed, depending on different profiles.
- **microservices** - The main directory for all microservices, can be broken down into individual folder for each microservie, e.g. `sample_service`.
  - [**microservice subfolder**] - Each microservice folder is a Docker container with [Skaffold](https://skaffold.dev/) + [Kustomize](https://kustomize.io/) to build images in different environments.
- **common** - The common image contains shared data models and util libraries used by all other microservices.

## Project Initialization

In your project folder, run the following to set up your project:
```
bash setup/setup_project.sh
```

This will run Terraform to create the following GCP resources:
- Enabling GCP services
- GKE Cluster and default node pool
- Service accounts for GKE cluster
- Firestore and backup bucket

Alternatively, you can run [Terraform](https://www.terraform.io/) manually with the following commands:
```
export BUCKET_NAME=$PROJECT_ID-tfstate
export BUCKET_LOCATION=us

cd terraform/environments/dev
terraform init -backend-config="bucket=$BUCKET_NAME"
terraform apply
```

Once Terraform completes the setup, you can verify those newly created GCP resources at the [GCP Console UI](https://console.developers.google.com/).

## Local develompent

### Initialization

For the first time, run the `setup_local.sh` to initialize required setup for local development. This will set up the kubectl as well as setting up the required Service Account permissions.

```
bash setup/setup_local.sh
```

### Run with all microservices

Set up the required environment variables.
```
export PROJECT_ID=<your-project>
export SKAFFOLD_NAMESPACE=default

# Or if you'd like to run with a different kubernetes namespace:
export SKAFFOLD_NAMESPACE=<another_namespace>
```

Deploy all microservices to the default GKE cluster:

```
skaffold dev

# Alternatively, you can run with a specific Skaffold profile and/or a custom image registry:
skaffold dev -p dev --default-repo=gcr.io/$PROJECT_ID
```

By default, it will deploy a `sample-service` microservice to the default GKE cluster.
- Open http://localhost:8888/sample_service/v1/docs in a browser window
- Verify if you see the Swagger API documentations

### Run with a specific microservice

Deploy a specific microservice to the default GKE cluster:

```
skaffold dev -m sample-service
```

Likewise, you can open http://localhost:8888/sample_service/v1/docs in a browser window to check if it deploys successfully.

## FAQ

TBD
