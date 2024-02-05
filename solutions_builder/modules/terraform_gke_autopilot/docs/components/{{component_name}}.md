# Module: Terraform GKE Stage

This module defines a Terraform GKE setup stage named "3-gke-autopillot".

Main components after setup:
- ./terraform/stage/3-gke-autopillot

## Setup

Run `st components add [COMPONENT_NAME]` to add this module.
```
cd my-solution-folder
sb components add terraform_gke_autopilot
```

Fill in the variables.
```
🎤 What is the name of this terraform stage?
   3-gke-autopillot
🎤 Which Google Cloud region?
   us-central1

...

Complete. Component terraform_gke added to solution at .
```

Initialize the terraform stage using `st init --stage=[STAGE_NAME]`
```
sb init --stage=3-gke
```

## Development

## FAQ


