# E2E testing for Template

This doc covers the setup and steps required for running e2e tests for Template. This is not for regular e2e test for development project generated from this template.

## Setup

> Currently we run into issues of creating brand new project for every e2e test. Hence we use one static project for e2e testing with resources clean up.

- Create an org-level service account as e2e-runner:
  > This service account can be created separately under another GCP project with granted permissions on the org-level.
  ```
  export E2E_RUNNER_PROJECT_ID=solutions-template-e2erunner
  export SA_EMAIL=solutions-template-e2e-runner@$E2E_RUNNER_PROJECT_ID.iam.gserviceaccount.com
  gcloud iam service-accounts create "solutions-template-e2e-runner" --project=${E2E_RUNNER_PROJECT_ID}
  ```

  Enable required services to the host project where the service account resides:
  ```
  gcloud services enable cloudresourcemanager.googleapis.com --quiet
  gcloud services enable cloudbilling.googleapis.com --quiet
  gcloud services enable container.googleapis.com --quiet
  gcloud services enable cloudbuild.googleapis.com --quiet
  ```

- Grant the service account with the following roles to the org-level IAM:
  - Organization Administrator
  - Organization Policy Administrator
  - Project IAM Admin
  - Service Usage Admin

- Create a project for running e2e test against.
  ```
  export PROJECT_ID=<e2e-test-project-id>
  gcloud projects create $PROJECT_ID
  gcloud config set project $PROJECT_ID
  ```

- Add IAM to the service account in $PROJECT_ID.
  ```
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/owner"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/resourcemanager.projectIamAdmin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/iam.serviceAccountAdmin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/storage.admin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/container.admin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/run.admin"
  gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SA_EMAIL}" --role="roles/run.invoker"
  ```

- Manually add `Organization Policy Administrator` role to the service account.

- Download the Service Account key (JSON).
  ```
  # Allow service account key creation.
  gcloud resource-manager org-policies disable-enforce constraints/iam.disableServiceAccountKeyCreation --project=$E2E_RUNNER_PROJECT_ID

  # Create new JSON key.
  gcloud iam service-accounts keys create .tmp/service-account-e2e-key.json --iam-account=$SA_EMAIL
  ```

- Remove previous application-default credentials.
  ```
  rm ~/.config/gcloud/application_default_credentials.json
  ```

- Log in with Service Account runner.
  ```
  export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/.tmp/service-account-e2e-key.json"
  gcloud auth activate-service-account $SA_EMAIL --key-file=$GOOGLE_APPLICATION_CREDENTIALS
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