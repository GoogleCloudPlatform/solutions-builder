# Cloud Run developmnet

## Deployment

In this Solutions Template, we use [`skaffold`](https://skaffold.dev/) to deploy for both backend microservices and frontend application. The same steps apply for deploying to GKE and Cloud Run.

### Deploy to Cloud Run with default **run.app** domain

Run the following to deploy Cloud Run with default Cloud Run URL:
```
export PROJECT_ID=<my-gcp-project-id>
export SERVICE_NAME=<service-name> # e.g. sample-service or frontend-angular

skaffold run -p cloudrun --default-repo=gcr.io/$PROJECT_ID -m $SERVICE_NAME
```

Once deployed, you will see the output like below:
```
Starting deploy...
 - configmap/env-vars-<hash> created
 - service/frontend-angular created
 - deployment.apps/frontend-angular created
Waiting for deployments to stabilize...
 - deployment/frontend-angular is ready.
Deployments stabilized in 1.932 second
You can also run [skaffold run --tail] to get the logs
```
Display the URL for the deployed Cloud Run services:
```
gcloud run services describe $SERVICE_NAME --region=$REGION
```
- This will display the following output:
  ```
  ✔ Service frontend-angular in region us-central1
  run-id:<id-hash>
  URL:     https://frontend-angular-<random-hash>.a.run.app
  Ingress: all
  Traffic:
    100% LATEST (currently frontend-angular-<hash>)
  ```
- You can also list all deployed Cloud Run services:
  ```
  gcloud run services list --region=us-central1 --format="value(name,status.url)"
  ```
- Skaffold uses the <project_number>-compute@developer.gserviceaccount.com Service Account for Cloud Run deployment. To run with a different service account, check out the **Optional: Manually deploy Microservices to CloudRun** section below.

Open up the URL like **https://frontend-angular-<hash>.a.run.app** in a browser to check out the frontend app.
- By default, Cloud Run services require authentication (e.g. Service Account) to access the services.
- To allow all users to access the frontend application from the Internet, follow the **Allowing public (unauthenticated) access to a Cloud Run service** section to allow public access.

### Deploy with live-reload for debugging

Run the following to build and deploy to Cloud Run with port forwarding to test via localhost:

```
export REGION=us-central1
skaffold dev -p cloudrun --default-repo=gcr.io/$PROJECT_ID -m $SERVICE_NAME --port-forward
```

Once deployed, you will see the output like below:
```
frontend-angular: Service starting: Deploying Revision. Waiting on revision frontend-angular-kmwth.
Cloud Run Service frontend-angular finished: Service started. 0/1 deployment(s) still pending
Forwarding service projects/solutions-template-develop/locations/us-central1/services/frontend-angular to local port 9001
Listing files to watch...
- frontend-angular
Press Ctrl+C to exit
Watching for changes...
```

Open the link http://127.0.0.1:9001 or http://localhost:9001 in a browser to see the service.
- If you are deploying the microservice, open http://localhost:9001/sample_service/docs for the API swagger documentation.
- At this point, every changes in local files will trigger files hot-swap and update to the remote instance automatically. See [Skaffold File Sync](https://skaffold.dev/docs/pipeline-stages/filesync/) for more details.
- When clicked Ctrl+C, it will remove the Cloud Run service.


### Allowing public (unauthenticated) access to a Cloud Run service

You can allow unauthenticated access to either the microservice or the frontend application.

Run the following commands to update Organization policies:
```
export ORGANIZATION_ID=$(gcloud organizations list --format="value(name)" | head -n 1)
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
```

Re-login to gcloud to refresh the auth:
```
gcloud auth application-default login
```

Run the following to allow unauthenticated users:
```
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

###  Optional: Manually deploy Microservices to CloudRun

Build common image
```
cd common
gcloud builds submit --config=cloudbuild.yaml --substitutions=\
_PROJECT_ID="$PROJECT_ID",\
_REGION="$REGION",\
_REPOSITORY="cloudrun",\
_IMAGE="common"
```

Build a service image
```
gcloud builds submit --config=cloudbuild.yaml --substitutions=\
_CLOUD_RUN_SERVICE_NAME=$SERVICE_NAME,\
_PROJECT_ID="$PROJECT_ID",\
_REGION="$REGION",\
_REPOSITORY="cloudrun",\
_IMAGE="$SERVICE_NAME",\
_SERVICE_ACCOUNT="<my-custom-sa>@$PROJECT_ID.iam.gserviceaccount.com",\
_ALLOW_UNAUTHENTICATED_FLAG="--allow-unauthenticated"
```

Deploy a microservice to CloudRun with public endpoint:
```
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

### Delete Cloud Run Services

To delete a specific Cloud Run service:
```
export SERVICE_NAME=sample-service
gcloud run services delete $SERVICE_NAME
```
