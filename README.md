# Google Cloud Solutions Builder

**A solution framework to generate code with built-in structure and modules
to accelerate your project setup.**

## TL;DR

Solutions Builder is a boilerplate tool for building repeatable solutions with the
best practices in architecture on Google Cloud, including Cloud Run, GKE clusters,
Test Automation, CI/CD, etc.

Solutions Builder provides built-in and ready-to-ship modules including:

- [Terraform](https://www.terraform.io/) boilerplate modules
- Modular microservice templates, deployable to Cloud Run or a Kubernetes cluster.
- Support using templates from remote Git repo (e.g. a private Git repo)
- Unified deployment using Skaffold.
- Auto-generated OpenAPI schema with [FastAPI](https://fastapi.tiangolo.com/).
- CI/CD deployment templates.

## Roadmap

Please see [Feature Requests in the GitHub issue list](https://github.com/GoogleCloudPlatform/solutions-builder/issues?q=is%3Aopen+is%3Aissue+label%3A%22feature+request%22).

## Prerequisite

| Tool       | Required Version | Installation                                         |
| ---------- | ---------------- | ---------------------------------------------------- |
| Python     | &gt;= 3.11       |                                                      |
| gcloud CLI | Latest           | https://cloud.google.com/sdk/docs/install            |
| Terraform  | &gt;= v1.3.7     | https://developer.hashicorp.com/terraform/downloads  |
| Skaffold   | &gt;= v2.4.0     | https://skaffold.dev/docs/install/#standalone-binary |

[Optional] For deploying to a GKE cluster, please install the following:

| Tool      | Required Version | Installation                                               |
| --------- | ---------------- | ---------------------------------------------------------- |
| Kustomize | &gt;= v5.0.0     | https://kubectl.docs.kubernetes.io/installation/kustomize/ |

## Install Solutions Builder CLI

With `pip`:

```
pip install solutions-builder
```

With `pipx`:

```
pip install --user pipx && pipx install solutions-builder
```

## Quick Start - Create a new solution

> This quick start steps will create the following:
>
> - Create a new solution folder.
> - Create a new GCP project and initialize Terraform infrastructure.
> - Add a FastAPI-based microservice with a sample API.
> - Deploy the service to Cloud Run.

Generate a new solution in `my-solution-folder` folder.

```
sb new my-solution-folder
```

This will prompt options and variables:

```
🎤 What is your project name? (Spaces are allowed.)
   my awesome solution name
🎤 What is your Google Cloud project ID?
   my-project-id
🎤 Create GCP project 'my-project-id'? (yes/no)
   yes
🎤 Which Google Cloud region?
   us-central1
🎤 Default deploy method? (cloudrun or gke)
   Cloud Run

(...Leave the rest as default)
```

Once answered, it will generate the code from the template:

```
Copying from template
    create  .
    create  .pylintrc
    create  .copier-answers.yml
    ...
```

Answer questions when adding `terraform_base` module:

```
Adding module 'terraform_base'...
🎤 Use GCS Bucket for Terraform backend?
   Yes

Copying from template
 identical  .
    create  terraform
    create  terraform/stages
    ...


Complete. New solution folder created at ./my-solution-folder.
```

Add a Sample Cloud Run microservice using `blank_service` module template:

```
cd my-solution-folder
sb add component sample_service -t blank_service
```

- Alternatively, use a template from a remote Git repo like:
  ```
   sb add component sample_service -t git@github.com:GoogleCloudPlatform/solutions-builder.git/modules/blank_service
  ```

And answer the following:

```
This will add component 'sample_service' to 'components' folder. Continue? [Y/n]:
🎤 Resource name (lower case, alphanumeric characters, '-')?
   sample-service
🎤 Which Google Cloud region?
   us-central1
🎤 Add a sample API?
   Yes
🎤 Does this component require the Common image?
   No
🎤 Default deploy method? (cloudrun or gke)
   Cloud Run
```

Initialize Terraform

```
sb terraform apply --all --yes
```

- This will initialize all Terraform stages.
- Build and deploy the sample service to Cloud Run.

Alternatively, build and deploy all components:

```
sb deploy
```

## CLI Usage

For more information on how to use the CLI, please refer to the [CLI_USAGE.md](docs/CLI_USAGE.md).

## Additional Guides

- [cloudshell.md](docs/guides/cloudshell.md) - Step-by-step guidance to run Solutions Builder on Google Cloud Shell.
- [cloudrun.md](docs/guides/cloudrun.md) - The guidance if you want to deploy microservice to Cloud Run.
- [gke.md](docs/guides/gke.md) - The overall development guidance on Google Kubernetes Engine.

## Development and contributions

- [CONTRIBUTIONS.md](CONTRIBUTIONS.md) - How to contribute this project, code submission process.
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Guidances on developing new templates, modules, and components.

## Troubleshooting

- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Development guide and code submission process.

## FAQ

- Who are the target audience/users for this Solutions Builder?

  - A: Any engineering team to start a new solution development project.

- Can I use this template for non-Google or multi-Cloud environments?
  - A: We design this Solutions Builder to work 100% out of the box with Google Cloud products. However, you could customize the solution to meet your needs on multi-Cloud environment. See [Why Google Cloud](https://cloud.google.com/why-google-cloud) for details.
