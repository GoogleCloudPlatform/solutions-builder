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
* CloudRun templates
* [In Progress] CI/CD deployment with CloudBuild

## Roadmap

Please see Feature Requests in the Github issue list at https://github.com/GoogleCloudPlatform/solutions-template/issues?q=is%3Aopen+is%3Aissue+label%3A%22feature+request%22

## Getting Started

### Prerequisites

Install Cookiecutter ([Github](https://github.com/cookiecutter/cookiecutter)):
- For MacOS:
  ```
  brew install cookiecutter
  ```

- For Windows, refer this [installation guide](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter)

- For unix (including [crostini](https://chromeos.dev/en/linux))
  ```
  pip3 install cookiecutter
  ```

Project requirements:

| Tool  | Current Version  | Documentation site |
|---|---|---|
| Skaffold   | v2.x    | https://skaffold.dev/ |
| Kustomize  | v4.3.1  | https://kustomize.io/ |
| gcloud CLI | Latest  | https://cloud.google.com/sdk/docs/install |

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

- **README.md** - This contains all details regarding the development and deployment for your particular project.
- **skaffold.yaml** - This is the master Skaffold YAML file that defines how everything is built and deployed, depending on different profiles.
- **microservices** - The main directory for all microservices, can be broken down into individual folder for each microservie, e.g. `sample_service`.
  - [**microservice subfolder**] - Each microservice folder is a Docker container with [Skaffold](https://skaffold.dev/) + [Kustomize](https://kustomize.io/) to build images in different environments.
- **common** - The common image contains shared data models and util libraries used by all other microservices.

### Getting started with the solution development

Once the solution skeleton code generated in the <project-id> folder, please follow the `README.md` inside **your project folder** to get started with the solution development,

## FAQ

- Who are the target audience/users for this Solutions template?
  - A: Any engineering team to start a new solution development project.
