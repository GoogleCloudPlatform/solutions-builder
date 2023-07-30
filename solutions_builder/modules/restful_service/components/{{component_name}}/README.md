# RESTful API microservice for {{data_model_plural | capitalize}} data model.

## Deploy

Use Solutions Builder CLI to deploy:
```
st deploy . --component {{component_name}}
```

Alternatively, deploy with Skaffold commandline:
```
skaffold run -p default -m {{component_name}}  --default-repo="gcr.io/{{project_id}}"
```

## Run locally

Create a virtualenv and install dependencies.
```
cd components/{{component_name}}
python -m virtualenv .venv
pip install -r requirements.txt
```

## Test

Run Firebase emulator in a separate terminial.
```
firebase emulators:start --only firestore --project fake-project
```

Install test related dependencies
```
pip install -r requirements.txt
```

Run pytest
```
pytest
```

## GKE configuration

### Deploy to GKE cluster

Connect to the GKE cluster
```
gcloud container clusters get-credentials main-cluster --region {{gcp_region}} --project {{project_id}}
```

Deploy with Skaffold using `gke` profile.

```
skaffold run -p gke -m {{component_name}}  --default-repo="gcr.io/{{project_id}}"
```

## Cloud Run configuration

### Update Cloud Run service to accept unauthenticated traffic

```
gcloud run services add-iam-policy-binding {{resource_name}} \
  --member="allUsers" \
  --role="roles/run.invoker"
```
