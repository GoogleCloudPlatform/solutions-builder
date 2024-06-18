# Solutions Builder CLI Usage

## Concept

### Copier-based templates

- All templates and modules are created using [Copier](https://copier.readthedocs.io/en/stable/).
- Each template folder (e.g. in /modules) has a `copier.yaml` to define questions and variables.

### sb.yaml

- Once creating a solution folder, it will create a `sb.yaml` file in the solution folder.
- When adding a new component/module, it will add the configuration for the component to the `sb.yaml` file.

### Components / Modules

- A component (or module) can be a Terraform module, a microservice (Python) module, or a frontend module.
- A template must have a `copier.yaml` to define variables
  and other configurations. You can still proceed if there's no
  `copier.yaml` in the template folder, but it will just copy
  entire folder without any modification.

There are three ways of adding a component:

- Add a component with built-in module template
- Add a component with a template in local folder
- Add a component with a template in remote Git repo

## Installation

With `pip`:

```
pip install solutions-builder
```

With `pipx`:

```
pip install --user pipx && pipx install solutions-builder
```

## Create a new solution folder

### Use the build-in template

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
🎤 What is your Google Cloud project number?
   12345678
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

### Use a template in local folder

To create a new solution folder with a template from a local folder, simply add `-t <path/to/template>` like below:

```
sb new my-solution-folder -t /path/to/my-template-folder
```

### Use a template with a remote Git repo

To create a new solution folder with a template a remote Git repo, add `-t <path/to/remote.git/folder>` like below:

```
sb new my-solution-folder -t git@github.com:GoogleCloudPlatform/solutions-builder.git/modules/blank_service
```

- This will download the Git repo automatically, and use the "subfolder" as the template path.

## Add a component

- A template must have a `copier.yaml` to define variables
  and other configurations. You can still proceed if there's no
  `copier.yaml` in the template folder, but it will just copy
  entire folder without any modification.

### List available built-in modules

```
sb list modules
```

This will show the following:

```
- blank_service
- cicd_github
- restful_service
- terraform_base
- terraform_gke
- terraform_gke_autopilot
- terraform_gke_ingress
- terraform_httplb_cloudrun
```

- **blank_service**: A FastAPI-based microservice as the skeleton for a backend API service.
- **restful_service**: A FastAPI-based microservice with a RESTful API for simple CRUD operations to Firestore data models.
- **cicd_github**: A template for CICD workflow using GitHub Actions.
- **terraform_base**: The foundation Terraform code for all solutions, including 1-bootstrap, 2-foundation and 3-application stages.
- **terraform_gke**: The module for GKE terraform
- **terraform_gke_autopilot**: The module for GKE Autopilot terraform
- **terraform_gke_ingress**: The module for GKE Ingress terraform
- **terraform_httplb_cloudrun**: The module for HTTP Load Balancer Cloud Run terraform

### Add a component

```
sb add component my_service -t restful_service
```

Answer the following questions (defined in `copier.yaml`)

```
🎤 Resource name (lower case, alphanumeric characters, '-')?
   my-service
🎤 The relative path used in ingress as http://my-domain/[service_path]
   my-service
🎤 Which Google Cloud region?
   us-central1
🎤 Data model name? (snake_case)
   todo
🎤 What's the plural form of the data model name? (snake_case)
   todos
🎤 Default deploy method? (cloudrun or gke)
   Cloud Run
🎤 Create network endpoint group (NEG) for serverless ingress?
   Yes
🎤 Does this component require the Common image?
   No
```

By default, it creates the component to `components/` folder.

### Add a component to a specific destination path

To create a component to a specific subfolder, e.g. `backend`:

```
sb add component my_service -t blank_service -d backend
```

### Add a component with a template in local folder

To create a component using a template from a local folder:

```
sb add component my_service -t /path/to/local/blank_service
```

### Add a component with a template in remote Git repo

To create a component using a template from a remote Git repo:

```
sb add component my_service -t git@github.com:GoogleCloudPlatform/solutions-builder.git/modules/blank_service
```

## Terraform modules

If you create a solution folder using `sb new <my-solution-folder>`, it will create the Terraform base module for you.

Check out the `terraform/stages` folder, you'll see the following subfolders:

- 1-bootstrap
- 2-foundation
- 3-application

The terraform code is broken down to `stages` for the following reason:

- Each stage is independent to other stages.
- Applying or destroying a stage will not affect the other stages.

### Adding a Terraform module

```
sb add terraform terraform_gke
```

- This will add the `terraform_gke` module to the `terraform` folder in a corresponding `stage`.

### Apply all Terraform stages

```
sb terraform apply --all
```

- Optionally, add `--yes` to the end of the command to skip the confirmation prompt. E.g.:

  ```
  sb terraform apply --all --yes
  ```

- This will init and apply all Terraform stages.

### Apply a specific Terraform stage

```
sb terraform apploy 3-application
```

### Destroy a specific Terraform stage

```
sb terraform destroy 3-application
```

## Advanced Scenarios

### Re-initialize sb.yaml

If you have an existing solution folder which is not created by Solutions Builder CLI, you can re-initialize sb.yaml by running:

```
sb init
```

Answer the following questions:

```
This will create a new 'sb.yaml' in '.'. Continue? [Y/n]:
🎤 What is your project name? (Spaces are allowed.)
   jonchen-sb-0616
🎤 What is your Google Cloud project ID?
   jonchen-sb-0616
🎤 What is your Google Cloud project number? (Leave it as empty if the project hasn't created yet.)
   262027426651
🎤 Which Google Cloud region?
   us-central1
🎤 Default deploy method? (cloudrun or gke)
   Cloud Run
🎤 Include a common container image for shared libraries, data models, utils, etc?
   No

Copying from template version None
 identical  .
    create  sb.yaml
```

It will create a new `sb.yaml` in the folder.

- Please note that it will preserve the `components` property if a `sb.yaml` exists in the folder.

## Global Variables

Global variables are defined in the `sb.yaml` and has anchors like `sb-vars:<var-name>` across all files in a module template.

For example, in `terraform/stages/1-bootstrap/terraform.tfvars`:

```
project_id          = "my-project-id" # sb-var:project_id
storage_multiregion = "US"
```

- Solution builder uses these anchor like `# sb-var:project_id` to define variables.
- When running `sb set-var project_id`, it scans for these anchors to replace the variables.

### Set and apply a global variable

You can add an anchor to specify where a variable to apply in the solution folder.

For example, in a YAML file:

```yaml
detail:
  PROJECT_ID: old-project-id # sb-var:project_id
  OTHER: something
```

- It sets a variable named "project_id" as the anchor for this "PROJECT_ID" property at the same line in the YAML file.

Then, you can run the following to replace the variable value:

```
sb set-var project_id new-project-id
```

- This will find all occurrence of the `sb-var:project_id` anchors in your folder, and replace with the new value "new-project-id"

The YAML file will become:

```yaml
detail:
  PROJECT_ID: new-project-id # sb-var:project_id
  OTHER: something
```

### Apply all existing global variables

You can apply all existing global variables to files with corresponding variable anchors.

For example, in a YAML file:

```yaml
detail:
  PROJECT_ID: old-project-id # sb-var:project_id
  OTHER: something
```

And in the `sb.yaml` file in your project root folder:

```yaml
global_variables:
  project_id: MY_PROJECT_ID
  project_name: core-solution-services
  project_number: MY_PROJECT_NUMBER
  gcp_region: us-central1
```

Run the following to apply all these values to existing variables in all files.

```
$ sb vars apply-all
```

All files with the corresponding anchors will be updated altogether.

### Set up project_id and project_number

```
sb set-project <my-project-id>
```

This will run the following:

- Update all `project_id` values.
- Retrieve the corresponding project number.
- Update all `project_number` values.

## For developer only

Check out the `solutions-builder` repo:

```
git clone git@github.com:GoogleCloudPlatform/solutions-builder.git
```

Optionally, create a virtualenv

```
virtualenv .venv
source .venv/bin/activate
```

Install with `poetry`

```
cd solutions-buidler
poetry install
```
