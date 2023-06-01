# Solutions Template - Installation

## Understanding Google Cloud

We recommend the following resources to get familiar with Google Cloud and microservices.

- What is [Microservice Architecture](https://cloud.google.com/learn/what-is-microservices-architecture)
- Kubernetes:
  - Learn about the [basics of Kubernetes](https://kubernetes.io/docs/concepts/overview/)
  - [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview) overview
  - [Skaffold](https://skaffold.dev/docs/), a command line tool that facilitates continuous development for container based & Kubernetes applications:
- Cloud Run:
  - Serverless container deployment and execution with [Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run)

## Installation

### Install dependencies

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

### Installing Solutions Template CLI

With `pip`:
```
pip install solutions-template
```

With `pipx`:
```
pip install --user pipx
pipx install solutions-template

# Alternatively, install a specific version
pipx install solutions-template==[version]
```

## Preparation

Optionally, you can create a brand new GCP project to start with a new solution, or use an existing GCP project:
```
# Optional: create a new GCP project. You can also use an existing GCP project.
gcloud projects create my-solution-gcp-id

# Set gcloud CLI to the GCP project.
gcloud config set project my-solutions-gcp-id
```

**NOTE**: Solutions Template will generate Infrastructure-as-Code (IaC) using Terraform.
It may contain GCP resource setup that conflicts with your existing resources.
We recommend starting with a brand new GCP project.

## Generate a new Solution folder

Run the following to generate a new solution skeleton at the current directory:
```
st new my-solution .
```

This will prompt options and variables:
```
🎤 What is your project name? (Spaces are allowed.)
   my-solution
🎤 What is your Google Cloud project ID?
   my-solution-gcp-id
    (Retrieving project number for my-solution-gcp-id...)
🎤 What is your Google Cloud project number?
   12345678
🎤 Which Google Cloud region?
   us-central1
🎤 Use GCS Bucket for Terraform backend?
   Yes
```

Once filled, it will generate a new folder `my-solution` with the following file structure:

```
├── .github
├── README.md
├── components
│   └── common
├── setup.cfg
├── skaffold.yaml
├── st.yaml
├── terraform
│   ├── modules
│   └── stages
│       ├── 1-bootstrap
│       ├── 2-foundation
│       └── 3-components
└── utils
```

- **README.md**: The default empty README for your project.
- **components/**: List of component/service folders. When adding components by running `st component add [COMPONENT_NAME]`, it will add a component subfolder here.
- **setup.cfg**: yapf python formatter.
- **skaffold.yaml**: Root skaffold YAML that manages deployment to Cloud Run and GKE.
- **st.yaml**: Root Solutions Template YAML that contains metadata for this solution folder.
- **terraform**: Infrastructure-as-Code using [Terraform](https://www.terraform.io/).
- **terraform/modules**: Terraform modules by Cloud resources.
- **terraform/stages**: Terraform stages based on [Cloud Foundation Fabric](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric) approach.

## Update an existing Solution folder

Solutions Template supports updating exsiting solution folder, however it may override your files. Please use it with caution.

Run the following to update an existing solution folder:

```
cd my-solution
st update .
```

This will prompt the same questions like in creating a new solution. You can provide a different values like a new GCP project ID or region. Once complete, it will replace the project ID and region to the exising solution folder.
```
🎤 What is your project name? (Spaces are allowed.)
   my-solution
🎤 What is your Google Cloud project ID?
   my-another-gcp-id
    (Retrieving project number for my-solution-gcp-id...)
🎤 What is your Google Cloud project number?
   12345678
🎤 Which Google Cloud region?
   us-east1
🎤 Use GCS Bucket for Terraform backend?
   Yes
```

## Initialize the solution infrastructure (terraform)

The default solution folder comes with two Terraform stages:
- 1-bootstrap
- 2-foundation

The `1-bootstrap` stage creates a GCS bucket for persisting terraform state file remotely. The `2-foundation` stage enables essential GCP APIs and creates basic resources like VPC netowrk, IAM roles, Firestore initialization, etc.

Run the following to initialize both stages:
```
st infra init
```
- Terraform will prompt for approval before proceed the terraform apply.
- You can also pass a `--yes` to automatically approve the changes.

Alternatively, to run a particular stage:
```
st infra apply [STAGE_NAME]
```

## Add a component

In Solutions Template, a component is a module provided with templated service (either frontend or backend) or templated Terraform code for particular GCP resources.

You can see the list of available component modules by run the following:
```
$ st component list

Available module names:

- restful_service
- terraform_gke
- terraform_httplb_cloudrun
```
- Alternatively you can check existing modules in [modules/](../solutions_template/modules) folder.

To add a component to a solution:
```
st component add [COMPONENT_NAME]
```

This will show the prompt quesitons from this particular component.

### Example: Add a Todo List RESTful API microservice

This section shows an example of adding RESTful API service component that manages Todo List data model.

For example, to add a RESTful microservice:
```
st component add restful_service
```

In the prompt, rename the component as `todo_service` (snake_case) and `todo-service` as resource name. (lower case with dash)
```
This will add component 'restful_service' to '.'. Continue? [Y/n]: Y
🎤 What is the name of this component (snake_case)?
   todo_service
🎤 Resource name (lower case, alphanumeric characters, '-')?
   todo-service
```

Then, provide the relative path that will be used in the Load balancer later.
```
🎤 The relative path used in http://my-domain/[service_path]
   todo-service
```

Choose the preferred GCP region:
```
🎤 Which Google Cloud region?
   us-central1
```

Here, we will input **`todo`** as the data model and its plural form. The CRUD operation will be handled by the RESTful API generated from the `restful_service` component template.
```
🎤 Data model name? (snake_case)
   todo
🎤 What's the plural form of the data model name? (snake_case)
   todos
```

In this example, we choose deploying to Cloud Run only. We will also need a Network Endpoint Group (NEG) to wire the Cloud Run service to a load balancer later.
```
🎤 Add Cloud Run to deployment methods (using Skaffold)?
   Yes
🎤 Create network endpoint group (NEG) for serverless ingress?
   Yes
🎤 Add GKE to deployment methods (using Skaffold)?
   No
🎤 Default deploy method? (cloudrun or gke)
   Cloud Run
```

This RESTful service does not depend on the Common library image at this moment. However other components may depend on `common` like `import common.models` or other common utils.
```
🎤 Does this component require the Common image?
   No
```

We'll leave other questions with default.
```
🎤 What's the port for local port forwarding?
   9001
🎤 Use Github Action as the default CI/CD?
   Yes
```

Once complete, it adds the `todo_service` folder to `my-solution/components`.
- It also add a `terraform/stages/3-httplb-cloudrun` which will be used later when adding a HTTP load balancer.

At this point, we'll deploy this service to Cloud Run with the following command:
```
st deploy
```
- This will run `skaffold run` to deploy all services with `default` profile.

Once complete, check the deployed Cloud Run services:
```
gcloud run services list
```

In addition, you can make this service public for testing purpose:
```
gcloud run services add-iam-policy-binding todo-service \
   --member="allUsers" \
   --role="roles/run.invoker" \
   --region="us-central1"
```
- NOTE: You may need to update the org policy to allow `constraints/iam.allowedPolicyMemberDomains` constraint.

Once updated, open the browser to the Cloud Run service's URL, and you'll see the link to the RESTful API swagger UI.

## Add an Infra component

An infra component is nothing but another component. Some component contains just infra pieces in `terraform/modules` or `terraform/stages` folders. Other component may contain both `component/service_name` as a microservice **AND** required infra resources in `terraform/stages`.

To add an infra component, run the same command like adding a regular component.
```
st component add [COMPONENT_NAME]
```

### Example: Add a HTTP load balancer

Run the following to add a HTTP load balancer that supports Google-managed cert and a domain name.
```
st component add terraform_httplb_cloudrun
```

Fill in the answers in the prompt.
```
This will add component 'terraform_httplb_cloudrun' to '.'. Continue? [Y/n]:
🎤 What is the name of this component?
   terraform_serverless_ingress
🎤 GCP region
   us-central1
🎤 DNS domains (comma-separated string)?
   my-solution-domain.com
    (Retrieving existing Cloud Run services for jonchenst-0530...)
🎤 Cloud Run service names as the LB backend? (comma-separated string)
   todo-service
```

This component creates a stage `3-httplb-cloudrun`, which you can find in `terraform/stages` folder.

To apply the infra terraform code:
```
st infra apply 3-httplb-cloudrun

... (terraform execution)

lb_https_ip_address = "12.34.56.78"
```
- This will create a HTTP load balancer with managed-cert using the given domain name.

Lastly, update your DNS with an **A record** to
match the external IP address returned value. You'd need to wait for a few minutes
for the DNS to refresh with new value.

Once the DNS is updated, you can open up the domain with a browser to see the full stack
in action.

