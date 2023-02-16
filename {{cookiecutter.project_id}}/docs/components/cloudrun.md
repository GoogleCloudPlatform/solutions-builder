# Cloud Run developmnet

## Deploy Microservices

TBD

## Deploy Frontend application

> Check out [more details here](https://skaffold.dev/docs/pipeline-stages/deployers/cloudrun/) for using skaffold to deploy Cloud Run.

### Deploy with live-reload for debugging

Run the following to build and deploy to Cloud Run with port forwarding to test via {{cookiecutter.api_domain}}:

```
export SERVICE_NAME=frontend-angular
export REGION={{cookiecutter.gcp_region}}

skaffold dev -p cloudrun --default-repo=gcr.io/$PROJECT_ID -m $SERVICE_NAME --port-forward
```

Once deployed, you will see the output like below:
```
frontend-angular: Service starting: Deploying Revision. Waiting on revision frontend-angular-kmwth.
Cloud Run Service frontend-angular finished: Service started. 0/1 deployment(s) still pending
Forwarding service projects/solutions-template-develop/locations/{{cookiecutter.gcp_region}}/services/frontend-angular to local port 8080
Listing files to watch...
- frontend-angular
Press Ctrl+C to exit
Watching for changes...
```

Open the link http://127.0.0.1:8080 or http://{{cookiecutter.api_domain}}:8080 in a browser to see the frontend app.

At this point, every changes in local files will trigger files hot-swap and update to the remote instance automatically. See [Skaffold File Sync](https://skaffold.dev/docs/pipeline-stages/filesync/) for more details.

When clicked Ctrl+C, it will remove the Cloud Run service.

### Deploy to Cloud Run with default **run.app** domain

Run the following to deploy Cloud Run with default Cloud Run URL:
```
skaffold run -p cloudrun --default-repo=gcr.io/$PROJECT_ID -m $SERVICE_NAME
```

Once deployed, you will see the output like below:
```
Cloud Run Service frontend-angular finished: Service started. 0/1 deployment(s) still pending
You can also run [skaffold run --tail] to get the logs
```

### Allowing public (unauthenticated) access to the frontend app

> By default, Cloud Run services require authentication (e.g. Service Account) to access the services. To allow all web users to access the frontend application, run the following to allow unauthenticated users.

Run the following commands to update Organization policies:
```
export ORGANIZATION_ID=$(gcloud organizations list --format="value(name)" | head -n 1)
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
```

Run the following to allow unauthenticated users:
```
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

Display the URL for the deployed Cloud Run services:
```
gcloud run services describe $SERVICE_NAME --region=$REGION
```
- This will display the following output:
  ```
  ✔ Service frontend-angular in region {{cookiecutter.gcp_region}}
  run-id:<id-hash>

  URL:     https://frontend-angular-<random-hash>.a.run.app
  Ingress: all
  Traffic:
    100% LATEST (currently frontend-angular-<hash>)
  ```

Open up the URL in a browser to check out the frontend app.


