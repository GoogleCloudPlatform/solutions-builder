1. [Installation Issues](#InstallationIssues)
##  1. <a name='InstallationIssues'></a>Installation Issues

### Apple M1 laptops related errors
- I use a Apple M1 Mac and got errors like below when I ran `terraform init`:
  ```
  │ Error: Incompatible provider version
  │
  │ Provider registry.terraform.io/hashicorp/template v2.2.0 does not have a package available for your current platform,
  │ darwin_arm64.
  │
  │ Provider releases are separate from Terraform CLI releases, so not all providers are available for all platforms. Other
  │ versions of this provider may have different platforms supported.
  ```
  - A: Run the following to add support of M1 chip ([reference](https://kreuzwerker.de/en/post/use-m1-terraform-provider-helper-to-compile-terraform-providers-for-mac-m1))
    ```
    brew install kreuzwerker/taps/m1-terraform-provider-helper
    m1-terraform-provider-helper activate
    m1-terraform-provider-helper install hashicorp/template -v v2.2.0
    ```

### gcloud CLI is stuck with the old project ID
- I ran terraform and other `gcloud` commands, it's stuck with old project ID.
  - A: First, check if gcloud is authorized correctly.
    ```
    gcloud auth list

    # This will show the config details below:
                        Credentialed Accounts
    ACTIVE  ACCOUNT
    *    jonchen@google.com
    ```

    If not, relogin to gcloud.
    ```
    gcloud auth login
    ```

    In addition, check if gcloud is set to the correct project:
    ```
    gcloud config list

    # This will show the config details below:
    [core]
    account = jonchen@google.com
    disable_usage_reporting = False
    project = my-project-id
    ```

    If not correct, set to the correct project ID.
    ```
    gcloud config set project my-project-id
    ```

    If the gcloud config is correct, run the following to check your application-default config:
    ```
    cat ~/.config/gcloud/application_default_credentials.json

    # This will show the following:
    {
      "client_id": "<hash-id>.apps.googleusercontent.com",
      "client_secret": "<client_secret>",
      "quota_project_id": "<project_id>",
      "refresh_token": "<refresh_token_hash>",
      "type": "authorized_user"
    }
    ```

    If not correct, re-login with application-default:
    ```
    gcloud auth application-default login

    # Alternatively, login with a service account:
    gcloud auth activate-service-account $SA_EMAIL --key-file=$GOOGLE_APPLICATION_CREDENTIALS
    ```

    Lastly, if you use Service account key, check if you have set GOOGLE_APPLICATION_CREDENTIALS.
    If yes, make sure it points to the correct credential JSON file.
    ```
    echo $GOOGLE_APPLICATION_CREDENTIALS
    export GOOGLE_APPLICATION_CREDENTIALS=<credential-json>
    ```

### Terraform error for acquiring the state lock
- I ran into the Terraform error for acquiring the state lock:
  ```
  │ Error: Error acquiring the state lock
  │
  │ Error message: writing "gs://<my-test-project>/stage/foundation/default.tflock" failed: googleapi: Error 412: At least one of the pre-conditions you specified did not hold., conditionNotMet
  │ Lock Info:
  │   ID:        <terraform-lock-id>
  │   Path:      gs://<my-test-project>/stage/foundation/default.tflock
  │   Operation: OperationTypeApply
  │   Who:       <my-user-name>
  │   Version:   1.3.7
  │   Created:   2023-02-09 23:41:22.565918 +0000 UTC
  │   Info:
  │
  │ Terraform acquires a state lock to protect the state from being written
  │ by multiple users at the same time. Please resolve the issue above and try
  │ again. For most commands, you can disable locking with the "-lock=false"
  │ flag, but this is not recommended.
  ╵
  ```

  In each terraform `stage` folder, run the folllowing:
  ```
  cd terraform/stages/foundation # foundation, gke or cloudrun.
  terraform force-unlock <terraform-lock-id>
  ```

### Terraform error when creating the jump host in 0-jumphost stage

- I ran into the following error when running `sb infra apply 0-jumphost`:
  ```
  │ Error: Error creating instance: googleapi: Error 412: Constraint constraints/compute.requireShieldedVm violated for project projects/jonchen-css-1004. Secure Boot is not enabled in the 'shielded_instance_config' field. See https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints for more information., conditionNotMet
  │
  │   with google_compute_instance.jump_host,
  │   on main.tf line 104, in resource "google_compute_instance" "jump_host":
  │  104: resource "google_compute_instance" "jump_host" {
  │
  ╵
  Error when running command:  terraform apply   (working_dir=./terraform/stages/0-jumphost)
  ```

  To fix this, run the following to update the organization policies (You will need Org Policy Admin IAM role.)
  ```
  export ORGANIZATION_ID=$(gcloud organizations list --format="value(name)")
  gcloud resource-manager org-policies delete constraints/compute.requireShieldedVm --organization=$ORGANIZATION_ID
  ```
