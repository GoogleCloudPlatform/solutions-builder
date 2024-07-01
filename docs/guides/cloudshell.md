# Using Solutions Builder in Google Cloud Shell

## Install dependencies

By default, Google Cloud Shell has the following installed (as of Jun 30th, 2024):

- Python 3.10
- Terraform v1.5.7
- Skaffold v2.11.1

Optionally, install the following for GKE cluster deployment.

```
wget https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh
sudo rm /usr/local/bin/kustomize
sudo ./install_kustomize.sh 5.0.0 /usr/local/bin
```

Install Solutions Builder:

```
pip3 install -U solutions-builder
```

- Make sure to run with python3 pip.

## Create a new GCP project

It's highly recommended to create a new GCP project before running Solutions Builder in a Google Cloud Shell.

- To avoid overriding the GCP resources in other existing project.

## Create a new solution

The following steps are the same as running Solutions Builder in your local environment.

```
sb new my-project-id
```

Then, add a component with the `blank_service` template:

```
sb add component test_service -t blank_service
```

Run the following to apply all terraforms, build and deploy to Cloud Run.

```
sb terraform apply --all --yes
```
