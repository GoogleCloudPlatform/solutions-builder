# E2E testing for Template

This doc covers the setup and steps required for running e2e tests for Template. This is not for regular e2e test for development project generated from this template.

## Setup

> Currently we run into issues of creating brand new project for every e2e test. Hence we use one static project for e2e testing with resources clean up.

- Create a project for running e2e test against.
  ```
  export PROJECT_ID=<e2e-test-project-id>
  gcloud projects create $PROJECT_ID
  gcloud config set project $PROJECT_ID
  ```

- Enable Cloud Resources and Billing services.
  ```
  gcloud services enable cloudresourcemanager.googleapis.com --quiet
  gcloud services enable cloudbilling.googleapis.com --quiet
  ```

- Using an org-level service account as e2e-runner:
  This service account is created separately under another GCP project with granted permissions on the org-level.
  ```
  export SA_EMAIL=solutions-template-e2e-runner@solutions-template-e2etest.iam.gserviceaccount.com
  ```

- Grant the service account with the following roles to the new e2e project:
  - Organization Administrator
  - Project IAM Admin
  - Service Usage Admin
  ```
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/resourcemanager.organizationAdmin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/orgpolicy.policyAdmin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/resourcemanager.projectIamAdmin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/serviceusage.serviceUsageAdmin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/iam.serviceAccountAdmin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/storage.admin"
  ```

- Download the Service Account key (JSON).
  ```
  # Allow service account key creation.
  gcloud resource-manager org-policies disable-enforce constraints/iam.disableServiceAccountKeyCreation --project=$PROJECT_ID

  # Create new JSON key.
  gcloud iam service-accounts keys create .tmp/service-account-e2e-key.json --iam-account=$SA_EMAIL
  ```

- Log in with Service Account runner.
  ```
  gcloud auth activate-service-account $SA_EMAIL --key-file=.tmp/service-account-e2e-key.json
  ```

## Run E2E tests locally

- Run e2e test
  ```
  bash ./e2e/template_e2e_tests/run_e2e_test.sh
  ```

## Run E2E tests with Github Actions for E2E tests

Add the following secrets to the `e2e` group:

- E2E_TEST_PROJECT_ID
- E2E_TEST_SA_KEY
