# Google Cloud Solutions Builder

**A solution framework to generate a new project with built-in structure and modules
to accelerate your project setup.**

## TL;DR

Solutions Builder is a boilerplate template for building repeatable
solutions with the best practices in architecture on Google Cloud, including GKE
clusters, Cloud Run, Test Automation, CI/CD, as well as development process.

This template provides built-in and ready-to-ship modules including:
* Easy-to-deploy [Terraform](https://www.terraform.io/) boilerplate modules
* Container-based microservices, can be deployed to a Kubernetes cluster or Cloud Run.
* Unified deployment using Skaffold.
* Automatically generated API documentation with Swagger UI.
* CI/CD deployment (with Github Actions).
* Cloud Run templates.

## Roadmap

Please see [Feature Requests in the Github issue list](https://github.com/GoogleCloudPlatform/solutions-builder/issues?q=is%3Aopen+is%3Aissue+label%3A%22feature+request%22).

## Prerequisite

| Tool | Required Version | Installation |
|---|---|---|
| Python     | &gt;= 3.9     | |
| gcloud CLI | Latest        | https://cloud.google.com/sdk/docs/install |
| Terraform  | &gt;= v1.3.7  | https://developer.hashicorp.com/terraform/downloads |
| Skaffold   | &gt;= v2.4.0  | https://skaffold.dev/docs/install/ |

[Optional] If you plan to deploy services on a GKE cluster, please install the following:

| Tool | Required Version | Installation |
|---|---|---|
| Kustomize   | &gt;= v5.0.0 | https://kubectl.docs.kubernetes.io/installation/kustomize/ |

## Installing Solutions Builder CLI

With `pip`:
```
pip install solutions-builder
```

With `pipx`:
```
pip install --user pipx
pipx install solutions-builder
```

## Quick Start

This quick start steps will do the following:
- Create a new GCP project and initialize Cloud foundation.
- Add a RESTful API service for managing Todo list.
- Deploy the service to Cloud Run.

Set up GCP project
```
export PROJECT_ID=my-solution-gcp-id

# (Optional) Create a new GCP project. You can also use an existing GCP project.
gcloud projects create $PROJECT_ID

# Set gcloud CLI to the GCP project.
gcloud config set project $PROJECT_ID
```

Generate a new solution folder.
```
sb new my-solution
```

This will prompt options and variables:
```
🎤 What is your project name? (Spaces are allowed.)
   my-solution
🎤 What is your Google Cloud project ID?
   my-solution-gcp-id
🎤 What is your Google Cloud project number?
   12345678
🎤 Which Google Cloud region?
   us-central1
🎤 Use GCS Bucket for Terraform backend?
   Yes
```

Go to the newly created project folder
```
cd my-solution
sb infra apply 1-bootstrap
```

Initialize Cloud infrastructure
- Option 1: (Recommended) Log in to the jump host and run the following command(s) in the solution folder.
- Option 2: Run the following commands in your local machine.
```
sb infra apply 2-foundation
```

Add a RESTful API service with **Todo** data model to this solution.
```
sb components add restful_service
```

Fill details in the prompt:
- Component name: **todo_service**
- Resource name: **todo-service**
- Relative path: **todo-service**
- GCP region: **us-central1**
- Data model name: **todo**
- Add Cloud Run to deployment methods: **yes**
- Create network endpoint group (NEG) for serverless ingress: **yes**
- Default deploy method? (cloudrun or gke): **Cloud Run**

Add a HTTP Load Balancer for Cloud Run service(s)
```
sb add component terraform_httplb_cloudrun
sb infra apply 3-httplb-cloudrun
```

Build and deploy
```
sb deploy
```
- See other deployment options in [solutions_builder/modules](solutions_builder/modules).


## Additional Documentations

You can find more documentations in [docs](docs) folder. In a nutshell, it covers the following:
- [INSTALLATION.md](docs/INSTALLATION.md) - The overall installation guide.
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide and code submission process.
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Development guide and code submission process.

In the [docs/components](docs/components/) folder, it contains a few more guidance based on each component/feature available in this template.
- [gke.md](docs/components/gke.md) covers the overall developmeng guidance on Google Kubernetes Engine.
- [cloudrun.md](docs/components/cloudrun.md) covers the guidance if you want to deploy microservice to Cloud Run.

## FAQ
- Who are the target audience/users for this Solutions Builder?
  - A: Any engineering team to start a new solution development project.

- Can I choose to deploy microservice just to Cloud Run?
  - A: Yes, please refer to [Setting up Google Cloud Project](README.md#setting-up-google-cloud-project) in this README.md to choose where to deploy microservices. Or you can refer to [INSTALLATION.md](docs/INSTALLATION.md) for more details.

- Can I use this template for non-Google or multi-Cloud environments?
  - A: We design this Solutions Builder to work 100% out of the box with Google Cloud products. However you could customize the solution to meet your needs on multi-Cloud environment. See [Why Google Cloud](https://cloud.google.com/why-google-cloud) for details.

## Troubleshoot

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for details.