# RESTful Service Module

A generic RESTful API service module that manages one data model in Firestore.

## What's in this module?

- A microservice component with RESTful API that manages CRUD operations on one data model.
- [Optional] A terraform stage that creates Network Endpoint Group used by HTTP Loadbalancer for Cloud Run deployment.
- Deployment with either Cloud Run or GKE cluster.
- Built-in Skaffold yamls for either Cloud Run or GKE deployment.

## Setup

### Add this module to a solution folder

To add a new RESTful service with a specific data model:
```
st components add restful_service
```

Fill details in the prompt:
- Component name: **todo_service**
- Resource name: **todo-service**
- Relative path: **todo-service**
- GCP region: **us-central1**
- Data model name: **todo**
- Add Cloud Run to deployment methods: **yes**
- Create network endpoint group (NEG) for serverless ingress: **yes**
- Default deploy method? (cloudrun or gke): **Cloud Run**

Once completed, it will add a new component folder
`components/[component_name]` in your solution folder.

### Update an existing module in a solution folder

```
st components update [component_name]
```

## Development

TODO: Add development guide.

## Deployment

TODO: Add deployment guide.

## Troubleshoot

TODO: Add troubleshooting details.

## Reference

TODO: Add reference.
