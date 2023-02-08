# Troubleshoots

## Installation Issues

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