# Task Dispatch Service Module

A RESTful API service module that manages tasks and dispatch tasks to microservices on GKE or Cloud Run based on the task's
status and context.

## What's in this module?

- A microservice component with RESTful API that manages CRUD operations on Task data model.
- Terraform stage that manages Pub/sub topic and EventArc trigger.
- Deployment with either Cloud Run or GKE cluster.
- Built-in Skaffold yamls for either Cloud Run or GKE deployment.

## Setup

### Add this module to a solution folder

To add a new RESTful service with a specific data model:
```
st components add task_dispatch_service
```

Fill details in the prompt:
- Component name: **task_dispatch_service**
- Resource name: **task-dispatch-service**
- Relative path: **task-dispatch-service**
- GCP region: **us-central1**
- Data model name: **task**
- Default deploy method? (cloudrun or gke): **GKE**

Once completed, it will add a new component folder
`components/[component_name]` in your solution folder.

### Update an existing module in a solution folder

```
st components update [component_name]
```

## Development

TODO: Add development guide.

## Deployment

### For GKE deployment

Deploy the microservice to GKE cluster.
```
st deploy --component=task_dispatch_service
```

Run Terraform for this stage.
```
st infra apply 3-task-dispatch
```
- This will create a Pub/Sub topic for tasks, and an EventArc to trigger for any published message on the Pub/Sub topic.

## Troubleshoot

TODO: Add troubleshooting details.

## Reference

TODO: Add reference.
