# Solutions Template

> This is the template for building packaged and repeatable solutions with
> the best practices in architecture on GCP, including GKE clusters, CI/CD,
> as well as development process.

# Getting Started

## Prerequisites

#### Install required packages

For MacOS:
```
brew install --cask skaffold kustomize google-cloud-sdk
```

For Windows:
```
choco install -y skaffold kustomize gcloudsdk
```

* Make sure to use __skaffold 1.21__ (Or 1.24.1) for development.

#### Set up kubectl context and namespace

Export GCP project id and the namespace based on your Github handle (i.e. user ID)
```
export PROJECT_ID=solutions-template
export SKAFFOLD_NAMESPACE=<Replace with your Github user ID>
```

Log in gcloud SDK:
```
gcloud auth login
```

Run the following to set up critical context and environment variables:

```
./setup/setup_local.sh
```

This shell script does the following:
- Set the current context to `gke_solutions-template_us-central1-a_default_cluster`. The default cluster name is `default_cluster`.
  > **IMPORTANT**: Please do not change this context name.
- Create the namespace $SKAFFOLD_NAMESPACE and set this namespace for any further kubectl operations. It's okay if the namespace already exists.
- Generate a Service Account JSON keyfile and add to the cluster.

## Run all microservices in `solutions-template` GKE cluster

> **_NOTE:_**  By default, skaffold builds with CloudBuild and runs in `solutions-template` GKE cluster, using the namespace set above.

To build and run in `solutions-template` cluster:
```
skaffold run --port-forward

# Or, to build and run in `solutions-template` cluster with hot reload:
skaffold dev --port-forward
```
- Please note that any change in the code will trigger the build process.

## Run with a specific microservice

```
skaffold run --port-forward -m <Microservice>
```

In this case, `Microservice` could be one of the following:
- Backend microservices:
  - `authentication`
  - `sample-service`

You can also run multiple specific microservices altogether. E.g.:

```
skaffold run --port-forward -m authentication,sample-service
```

## Deploy to a specific GKE cluster

> **IMPORTANT**: Please change gcloud project and kubectl context before running skaffold.

Replace the `<Custom GCP Project ID>` with a specific project ID and run the following:
```
export PROJECT_ID=<Custom GCP Project ID>

# Switch to a specific project.
gcloud config set project $PROJECT_ID

# Assuming the default cluster name is "default_cluster".
gcloud container clusters get-credentials default_cluster --zone us-central1-a --project $PROJECT_ID
```

Run with skaffold:
```
skaffold run -p custom --default-repo=gcr.io/$PROJECT_ID

# Or run with hot reload and live logs:
skaffold dev -p custom --default-repo=gcr.io/$PROJECT_ID
```

## Run with local minikube cluster

Install Minikube:

```
# For MacOS:
brew install minikube

# For Windows:
choco install -y minikube
```

Make sure the Docker daemon is running locally. To start minikube:
```
minikube start
```
- This will reset the kubectl context to the local minikube.

To build and run locally:
```
skaffold run --port-forward

# Or, to build and run locally with hot reload:
skaffold dev --port-forward
```

Optionally, you may want to set `GOOGLE_APPLICATION_CREDENTIALS` manually to a local JSON key file.
```
GOOGLE_APPLICATION_CREDENTIALS=<Path to Service Account key JSON file>
```

## Useful Kubectl commands

To check if pods are deployed and running:
```
kubectl get po

# Or, watch the live update in a separate terminal:
watch kubectl get po
```

To create a namespace:
```
kubectl create ns <New namespace>
```

To set a specific namespace for further kubectl operations:
```
kubectl config set-context --current --namespace=<Your namespace>
```
