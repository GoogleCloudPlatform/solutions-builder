# GKE developmnet

## Deploy Microservices

TBD

## Deploy Frontend application

### Deploy with live-reload for debugging

To deploy to remote GKE cluster with local port-forwarding:
```
skaffold dev --default-repo=gcr.io/$PROJECT_ID -m frontend-angular
```

You will see the following output with the local port-forwarding endpoint:
```
Starting deploy...
- configmap/env-vars-<hash> unchanged
- service/frontend-angular configured
- deployment.apps/frontend-angular configured
Waiting for deployments to stabilize...
- deployment/frontend-angular is ready.
Deployments stabilized in 1.927 second
Port forwarding service/frontend-angular in namespace default, remote port 80 -> http://127.0.0.1:8080
Listing files to watch...
- frontend-angular
Press Ctrl+C to exit
[frontend-angular] 10.1.0.1 - - [15/Feb/2023:22:42:23 +0000] "GET / HTTP/1.1" 200 551 "-" "kube-probe/1.23"
Watching for changes...
```

Open the link http://127.0.0.1:8080 or http://{{cookiecutter.api_domain}}:8080 in a browser to see the frontend app.

At this point, every changes in local files will trigger files hot-swap and update to the remote instance automatically. See [Skaffold File Sync](https://skaffold.dev/docs/pipeline-stages/filesync/) for more details.

### Deploy to GKE cluster

Once you complete the development, run the following to deploy to remote GKE cluster:
```
skaffold run --default-repo=gcr.io/$PROJECT_ID -m frontend-angular
```

The next step is to update the ingress object with the rule for the frontend app endpoint.

