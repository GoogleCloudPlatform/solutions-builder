<!-- vscode-markdown-toc -->
* 1. [Installation Issues](#InstallationIssues)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc --># Troubleshoots

##  1. <a name='InstallationIssues'></a>Installation Issues

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

- I ran terraform and other `gcloud` commands, it's stuck with old project ID.
  - A: First, check if gcloud is set to the correct project:
    ```
    gcloud auth list

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
      "quota_project_id": "solutions-template-e2etest",
      "refresh_token": "<refresh_token-hash>",
      "type": "authorized_user"
    }
    ```

    If not correct, re-login with application-default:
    ```
    gcloud auth application-default login
    ```
