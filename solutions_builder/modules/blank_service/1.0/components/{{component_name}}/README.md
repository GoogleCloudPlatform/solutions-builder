# {{component_name}} Microservice

## Development

### Run locally

Create a virtualenv and install dependencies.
```
cd components/{{component_name}}
python -m virtualenv .venv
pip install -r requirements.txt
```

If this service depends on **components/common**, run the following
to install all dependencies from common.

```
pip install -r ../common/requirements.txt
```

Run `main.py`.
```
cd components/{{component_name}}/src
PYTHONPATH=../common/src python main.py
```

### Deploy to remote GKE cluster with livereload

Use Solutions Builder CLI to deploy:
```
st deploy . -m {{component_name}} --dev
```

Alternatively, deploy with Skaffold command:
```
skaffold dev -p default -m {{component_name}}  --default-repo="gcr.io/{{project_id}}"
```

## Test

If this microservice uses Firestore, run Firebase emulator in a separate terminial.
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

## Deploy

### Deploy to remote GKE cluster or Cloud Run

Use Solutions Builder CLI to deploy:
```
st deploy . -m {{component_name}}
```

Alternatively, deploy with Skaffold command:
```
skaffold run -p default -m {{component_name}}  --default-repo="gcr.io/{{project_id}}"
```

