# RESTful API microservice for {{data_model_plural | capitalize}} data model.

## Deploy

Use Solutions Template CLI to deploy:
```
st deploy . --component {{component_name}}
```

Alternatively, deploy with Skaffold commandline:
```

```

## Run locally

## Test

Run Firebase emulator in a separate terminial.
```
firebase emulators:start --only firestore --project fake-project
```

Run pytest
```
pytest
```