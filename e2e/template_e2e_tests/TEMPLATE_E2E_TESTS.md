# E2E testing for Template

This doc covers the setup and steps required for running e2e tests for Template. This is not for regular e2e test for development project generated from this template.

## Setup

> Currently we run into issues of creating brand new project for every e2e test. Hence we use one static project for e2e testing with resources clean up.

- Create a project for running e2e test against.
  ```
  export PROJECT_ID=<e2e-test-project-id>
  ```
- Create a service account as e2e-runner:
  ```
  gcloud iam service-accounts create "solutions-template-e2e-runner"
  export SA_EMAIL=solutions-template-e2e-runner@$PROJECT_ID.iam.gserviceaccount.com
  ```
- Grant the service account with the following roles
  - Organization Administrator
  - Project Deleter
  - Project IAM Admin
  - Service Usage Admin
- Download the Service Account key (JSON).
  ```
  # Allow service account key creation.
  gcloud resource-manager org-policies disable-enforce constraints/iam.disableServiceAccountKeyCreation --organization=$ORGANIZATION_ID

  # Create new JSON key.
  gcloud iam service-accounts keys create .tmp/service-account-e2e-key.json --iam-account=$SA_EMAIL
  ```
- Log in with Service Account runner.
  ```
  export GOOGLE_APPLICATION_CREDENTIALS=.tmp/service-account-e2e-key.json
  gcloud auth activate-service-account $SA_EMAIL --key-file=$GOOGLE_APPLICATION_CREDENTIALS
  ```

- Add Storage IAM permission to the Service Account.
  ```
  gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role='roles/storage.admin' --quiet
  ```

## Run E2E tests

- Run e2e test
  ```
  export ORGANIZATION_ID=<your-org-id>
  export FOLDER_ID=<your-folder-id>
  export BILLING_ACCOUNT=<your-billing-id>
  sh run_e2e_test.sh
 ```



