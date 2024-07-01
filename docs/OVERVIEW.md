# Solutions Builder Overview

## Concept

### Copier and Jinja templates

- All templates and modules are created using [Copier](https://copier.readthedocs.io/en/stable/).
- Each template folder (e.g. in /modules) has a `copier.yaml` to define questions and variables.
- [Copier](https://copier.readthedocs.io/en/stable/) uses Jinja for template syntax.

### sb.yaml

- Once creating a solution folder, it will create a `sb.yaml` file in the solution folder.
- When adding a new component/module, it will add the configuration for the component to the `sb.yaml` file.

## Components

- A component can be a Terraform module, a microservice (Python) module, or a frontend module, etc.
- A template folder must have a `copier.yaml` to define variables
  and other configurations. You can still proceed if there's no
  `copier.yaml` in the template folder, but it will just copy
  entire folder without any modification.

There are three ways of adding a component:

- Add a component with built-in module template
- Add a component with a template in local folder
- Add a component with a template in remote Git repo

### Adding a component with built-in module template

Run the following to add a component with built-in module template:

```
sb add component my_component_name -t blank_service
```

- This will create a new component called `my_component_name` with `blank_service` as the template.
- The `blank_service` module is one of the built-in modules in Solutions Builder.

### Adding a component with a template in local folder

Run the following to add a component with a template in local folder:

```
sb add component my_component_name -t /path/to/module
```

- This will create a new component called `my_component_name` with the module template in `/path/to/module`.
- The folder `/path/to/module` requires a `copier.yaml`. See the [Copier template] section below.

### Adding a component with a template in remote Git repo

Run the following to add a component with a template in local folder:

```
sb add component my_component_name -t git@github.com:GoogleCloudPlatform/solutions-builder.git/modules/blank_service
```

- This will create a new component called `my_component_name` with the module template in remote git repo `git@github.com:GoogleCloudPlatform/solutions-builder.git` with subfolder `modules/blank_service`.

## Copier template

Solutions Builder is built with [Copier](https://copier.readthedocs.io/en/stable/), which uses Jinja for template syntax. Each module folder has a `copier.yaml` that defines the questions and variables
that Copier will replaces with.

For example, a microservice module folder has following files:

```
├── copier.yaml
├── skaffold.yaml.patch
├── terraform
│   └── stages
│       └── 3-application
│           └── {{component_name}}_cloudrun.tf
└── components
    └── {{component_name}}
        ├── Dockerfile
        ├── README.md
        ├── requirements.txt
        ├── skaffold.yaml
        ├── src
        └── manifests
            └── cloudrun-service.yaml
```

`copier.yaml` defines the questions (variables) in this module:

```
component_name:
  type: str
  help: What is the name of this component (snake_case)?
  default: my_service
  validator: "{% if not component_name %}Required{% endif %}"

region:
  type: str
  help: Which Google Cloud region?
  default: us-central1

deploy_method:
  type: str
  help: Default deploy method? (cloudrun or gke)
  choices:
    Cloud Run: cloudrun
    GKE: gke
  default: cloudrun

...

```

When adding a module from a Copier template, it will ask questions for
these variables:

```

🎤 What is the name of this component (snake_case)?
    test_service
🎤 Which Google Cloud region?
    us-central1
🎤 Default deploy method? (cloudrun or gke)
    Cloud Run

```

These variables (e.g. `component_name`, `region`, etc) will be used in Jinja templates like below:

```
# terraform/stages/3-application/{{component_name}}\_cloudrun.tf

resource "google_cloud_run_v2_service" "{{component_name}}" {
  depends_on = [
    null_resource.{{component_name}}_build_container
  ]
  name     = "{{resource_name}}"
  project  = var.project_id
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/${var.project_id}/default/{{resource_name}}:latest"
    }
  }
}

```

- Variables like `{{component_name}}`, `{{region}}`, etc. will be replaced with the value given by the user.

In `copier.yaml`, it also defines other configurations:

- `_answers_file` defines where to put the answer.yaml file.

  ```
  _answers_file: ".sb/component_answers/{{component_name}}.yaml"
  ```

  - This YAML stores the answered values for each variables from `copier.yaml`.

- `_templates_suffix` is set as empty string so Copier will process all file with any extensions.
- `_patch` is used by Solutions Builder to "patch" files with delta instead of overwriting.
  ```
  _patch:
    - "skaffold.yaml"
  ```
  - In the example above, this template will patches `skaffold.yaml` by appending content to the end of the file.
- `_exclude` defines a list of files (regex) to exclude. See [Copier docs](https://copier.readthedocs.io/en/stable/configuring/#exclude) for more details.

- `_jinja_extensions` defines list of extensions for additional Jinja functions. In Solutions Builder, it uses a custom extension file with several helper functions.
  ```
  _jinja_extensions:
  - jinja2_time.TimeExtension
  - jinja2_strcase.StrcaseExtension
  - copier_templates_extensions.TemplateExtensionLoader
  - ../../copier_extensions/sb_helpers.py:SolutionsTemplateHelpersExtension
  ```
  - `copier_extensions/sb_helpers.py` contains the custom helper functions. See [Copier docs](https://copier.readthedocs.io/en/stable/configuring/#jinja_extensions) for more details.

## Building & deploying with Skaffold

Solutions Builder uses [Skaffold](https://skaffold.dev) as the deployment orchestration tool. See https://skaffold.dev for more details.

In a nutshell, Skaffold simplifies the process of building and deploying steps:

- Builds Docker images
- Push container images to Artifact Registry
- Deploy images to Cloud Run or a Kubernetes cluster.
- Optionally, deploy a image with local port forwarding for local troubleshooting.

Traditionally, each step requires one or a few commands, and requires a numbers of parameters.
Skaffold simplifies all the steps to one command like below:

```
skaffold run -p cloudrun --default-repo="us-docker.pkg.dev/my-project-id/default"
```

- This command will build, upload, and deploy image to Cloud Run.

### Root skaffold.yaml

In Solutions Builder, it uses 2-layer Skaffold configuration files for overall solution vs. individual component.

E.g. the file structure looks like below:

```
├── sb.yaml
├── skaffold.yaml  # root skaffold.yaml
├── components
│   └── test_service
│       ├── Dockerfile
│       ├── skaffold.yaml # component skaffold.yaml
│       └── src
│           ├── ...
└── ...

```

- A root `skaffold.yaml` in the root solution folder.
- Each component (e.g. a microservice folder) has its own `skaffold.yaml`.

In the root `skaffold.yaml`, it defines where to find other components:

```
apiVersion: skaffold/v4beta1
kind: Config
metadata:
  name: all-services
requires:
- configs:
  - test_service
  path: ./components/test_service
```

- `requires` defines a list of configs with name and path for each component.

When adding a new component, it will patch a new config and path to the end of the requires list. This is defined in the `copier.yaml` in a module:

```
_patch:
  - "skaffold.yaml"
```

A `skaffold.yaml.path` in a module template looks like this:

```
requires:
  - configs:
      - {{component_name}}
    path: ./{{destination_path}}/{{component_name}}

```

- When adding a component, Solutions Builder will merge the patch file to the root `skaffold.yaml`.
- See [blank_service/skaffold.yaml](../../solutions_builder/modules/blank_service/skaffold.yaml.patch) for an example.

### skaffold.yaml in modules

Skaffold uses `skaffold.yaml` to define all steps with several sections. E.g.:

```
apiVersion: skaffold/v4beta1
kind: Config
metadata:
  name: test_service

# This section defines how it builds Docker images.
build:
  ...

# This section defines a list of profiles for different deploy methods.
profiles:
- name: cloudrun
  ...

- name: gke
  ...
```

In the `build` section:

```
build:
  artifacts:
  - image: test-service
    sync:
      infer:
      - '**/*.py'
      - '**/*.json'
    docker:
      cacheFrom:
      - test-service
      - test-service:latest
  googleCloudBuild: {}

```

- `artifacts` sub-section defines the following:
  - `image` defines the image name that will be used and uploaded to the
    Artifact Registry.
  - `sync` is for remote hot-reload, useful for remote troubleshooting. See [File Sync](https://skaffold.dev/docs/filesync/) for more info.
  - `docker` defines how it build Docker images using Dockerfile and usage of caching.
- When `googleCloudBuild` presents, it will use GCP Cloud Build to build the docker images.
  - It leaves `{}` to set default Cloud Build configuration.

In the `profiles` section, it defines one or more "profiles":

```
profiles:

# Profile for Cloud Run deployment, building images via CloudBuild
- name: cloudrun
  manifests:
    rawYaml:
      - manifests/cloudrun-service.yaml
  deploy:
    cloudrun:
      projectid: my-project-id
      region: us-central1
  portForward:
  - resourceType: service
    resourceName: test-service
    port: 80
    localPort: 9001 # For local port forwarding

```

In the `cloudrun` profile, it defines where to find the manifest YAML, how to deploy, and optionally the local port-forwarding config.

- `name` - Profile name.
- `manifests` - Cloud Run service YAML in `manifests/cloudrun-service.yaml`
- `deploy` - Project ID and region.
- `portForward` - Local port forwarding config.

See [Skaffold - Cloud Run](https://skaffold.dev/docs/deployers/cloudrun/) for more info.
