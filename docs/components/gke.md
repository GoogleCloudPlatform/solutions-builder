# GKE developmnet

## Deployment

In this Solutions Template, we use [`skaffold`](https://skaffold.dev/) to deploy for both backend microservices and frontend application. The same steps apply for deploying to GKE and Cloud Run.

### Initialize GKE cluster

If you haven't set up the GKE cluster by following the [INSTALLATION.md](../INSTALLATION.md#SetupanddeploySolutionsTemplateAutomated), you can initialize GKE cluster via Terraform. This will create the following resources:
- A GKE cluster
- Service account for GKE

```
cd $BASE_DIR/terraform/stages/gke
terraform init -backend-config=bucket=$TF_BUCKET_NAME
terraform apply -auto-approve
```

### Deploy a service to GKE cluster

Once you complete the development, run the following to deploy to remote GKE cluster:
```
export PROJECT_ID=<my-gcp-project-id>
export SERVICE_NAME=<service-name> # e.g. sample-service or frontend-angular

skaffold run -p gke --default-repo=gcr.io/$PROJECT_ID -m $SERVICE_NAME
```

Update the ingress with new rules for this deployed service:
- TBD

### Deploy to GKE cluster with live-reload for debugging

To deploy to remote GKE cluster with local port-forwarding:
```
skaffold dev -p gke --default-repo=gcr.io/$PROJECT_ID -m sample-service
```

You will see the following output with the local port-forwarding endpoint:
```
Starting deploy...
- configmap/env-vars-<hash> unchanged
- service/sample-service configured
- deployment.apps/sample-service configured
Waiting for deployments to stabilize...
- deployment/sample-service is ready.
Deployments stabilized in 1.927 second
Port forwarding service/sample-service in namespace default, remote port 80 -> http://127.0.0.1:9001
Listing files to watch...
- sample-service
Press Ctrl+C to exit
[sample-service] 10.1.0.1 - - [15/Feb/2023:22:42:23 +0000] "GET / HTTP/1.1" 200 551 "-" "kube-probe/1.23"
Watching for changes...
```

Open the link http://127.0.0.1:PORT or http://localhost:PORT in a browser to see the service. (PORT will be different for each service)
- If you are deploying a microservice, open http://localhost:9001/sample_service/docs for the API swagger documentation.
- If you are deploying a frontend service, open http://localhost:8080 to see the web UI.
- At this point, every changes in local files will trigger files hot-swap and update to the remote instance automatically. See [Skaffold File Sync](https://skaffold.dev/docs/pipeline-stages/filesync/) for more details.
- When clicked Ctrl+C, it will remove the Cloud Run service.

## Design

### Terraform GKE Stage

### Skaffold

### Kustomzie + Kpt

## Troubleshoot

### Kubernetes Service Account

#### Access denied to Firestore in the Sample Service (Kubernetes Pod)

If you're seeing the following in the logs from Sample Service as below:
```
google.api_core.exceptions.PermissionDenied: 403 Missing or insufficient permissions.
```
this is because the particular Kubernetes pod (sample-service in this case) does not have the correct setup of kubernetes identity worload to access GCP resources.

Most of the operation within a Kubernetes pod is authenticated through workload identity with a service account. Run the following to double check the Kubernetes service account:

```
# Describe the services account name "gke-sa" registered in Kubernetes:
kubectl describe sa/gke-sa
```

This will display the detail of this service account:
```
Name:                gke-sa
Namespace:           default
Labels:              <none>
Annotations:         iam.gke.io/gcp-service-account: gke-sa@$PROJECT_ID.iam.gserviceaccount.com
Image pull secrets:  <none>
Mountable secrets:   gke-sa-token-<token-hash>
Tokens:              gke-sa-token-<token-hash>
Events:              <none>
```

Next, verify if the service account exists in the GCP project:
```
gcloud iam service-accounts describe gke-sa@$PROJECT_ID.iam.gserviceaccount.com
```

And check all roles this service account has:
```
gcloud projects get-iam-policy $PROJECT_ID \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:gke-sa@$PROJECT_ID.iam.gserviceaccount.com"
```

For any missing permissions, add roles in `service_account_roles` in the [Terraform GKE stage](../../terraform/stages/gke/main.tf)
```
module "gke" {
  ...

  # Add new roles to the GKE service account:
  service_account_roles = [
    "roles/aiplatform.user",
    "roles/bigquery.admin",
    "roles/datastore.owner",
    "roles/documentai.admin",
    "roles/firebase.admin",
    "roles/iam.serviceAccountUser",
    "roles/logging.admin",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/pubsub.admin",
    "roles/stackdriver.resourceMetadata.writer",
    "roles/storage.admin",
  ]
}
```

Once added, re-run the GKE terraform stage, following the steps in [Initialize GKE cluster](#initialize-gke-cluster) section above.
