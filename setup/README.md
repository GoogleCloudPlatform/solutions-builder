# Setting up a new cluster for AI-Tutor application

## Before you begin

Install `gcloud` CLI:
```
brew install --cask google-cloud-sdk
```
Or, check out [this installation guide](https://cloud.google.com/sdk/docs/installhttps://cloud.google.com/sdk/docs/install).

Then, log in to GCP:
```
gcloud auth application-default login
```

## To set up GKE cluster

Run the following to create the cluster and necessary settings.
- Please replace the variables accordingly.
```
PROJECT_ID=<GCP Project ID> bash ./setup/setup_cluster.sh
```

Run the following to set up ingres and certs.
```
PROJECT_ID=<GCP Project ID> \
  EMAIL=jonchen@google.com \
  WEB_APP_DOMAIN=<GCP Project ID>.cloudpssolutions.com \
  API_DOMAIN=<GCP Project ID>-api.cloudpssolutions.com \
  bash ./setup/setup_ingress.sh
```

## To set up for local development

```
bash ./setup_local.sh
```
