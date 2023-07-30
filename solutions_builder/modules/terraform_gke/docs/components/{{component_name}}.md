# Module: Terraform GKE Stage

This module defines a Terraform GKE setup stage named "2-gke".

Main components after setup:
- ./terraform/stage/2-gke

## Setup

Run `st components add [COMPONENT_NAME]` to add this module.
```
cd my-solution-folder
st components add terraform_gke .
```

Fill in the variables.
```
🎤 What is the name of this terraform stage?
   2-gke
🎤 Which Google Cloud region?
   us-central1
🎤 Kubernetes version?
   1.24.11-gke.1000
🎤 Allow domains for CORS? (comma-seperated)
   http://localhost:4200,http://localhost:3000
🎤 Cert Issuer Email
   my_name@example.com

...

Complete. Component terraform_gke added to solution at .
```

Initialize the terraform stage using `st init --stage=[STAGE_NAME]`
```
st init --stage=2-gke
```

## Development

## FAQ


