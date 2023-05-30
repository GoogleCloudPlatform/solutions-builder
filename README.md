# Google Cloud Solutions Template

**A solution framework to generate a new project with built-in structure and modules
to accelerate your project setup.**

## TL;DR

Solutions Template is a boilerplate template for building repeatable
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

Please see [Feature Requests in the Github issue list](https://github.com/GoogleCloudPlatform/solutions-template/issues?q=is%3Aopen+is%3Aissue+label%3A%22feature+request%22).

## Prerequisite

| Tool  | Required Version | Documentation site |
|---|---------------|---|
| Python              | &gt;= 3.9              | https://www.python.org/downloads/release/python-390/ |
| gcloud CLI          | Latest                 | https://cloud.google.com/sdk/docs/install |
| Terraform           | &gt;= v1.3.7           | https://developer.hashicorp.com/terraform/downloads |


## Installing Solutions Template CLI

```
pipx install solutions-template
```

## Getting Started

Generate a new solution folder.
```
st new my-solution .
```

This will prompt options and variables:
```
🎤 What is your project name? (Spaces are allowed.)
   my-solutions
🎤 What is your Google Cloud project ID?
   my-solutions
🎤 What is your Google Cloud project number?
   12345678
🎤 Which Google Cloud region?
   us-central1
🎤 Use GCS Bucket for Terraform backend?
   Yes
```

Go to the newly created project folder and initialize the solution.
```
cd my-solution
st init
```

Add a RESTful API component with **Todo** data model to this solution.
```
st component add restful_service
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
st add component terraform_httplb_cloudrun
st init --stage=3-httplb-cloudrun
```

Build and deploy
```
st deploy
```
- See other deployment options in ____.


## Additional Documentations

You can find more documentations in [docs](docs) folder. In a nutshell, it covers the following:
- [INSTALLATION.md](docs/INSTALLATION.md) - The overall installation guide.
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide and code submission process.
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Development guide and code submission process.

In the [docs/components](docs/components/) folder, it contains a few more guidance based on each component/feature available in this template.
- [gke.md](docs/components/gke.md) covers the overall developmeng guidance on Google Kubernetes Engine.
- [cloudrun.md](docs/components/cloudrun.md) covers the guidance if you want to deploy microservice to Cloud Run.

## FAQ
- Who are the target audience/users for this Solutions template?
  - A: Any engineering team to start a new solution development project.

- Can I choose to deploy microservice just to Cloud Run?
  - A: Yes, please refer to [Setting up Google Cloud Project](README.md#setting-up-google-cloud-project) in this README.md to choose where to deploy microservices. Or you can refer to [INSTALLATION.md](docs/INSTALLATION.md) for more details.

- Can I use this template for non-Google or multi-Cloud environments?
  - A: We design this Solutions Template to work 100% out of the box with Google Cloud products. However you could customize the solution to meet your needs on multi-Cloud environment. See [Why Google Cloud](https://cloud.google.com/why-google-cloud) for details.

## Troubleshoot

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for details.