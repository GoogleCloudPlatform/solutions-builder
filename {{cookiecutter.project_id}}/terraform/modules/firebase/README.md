## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | n/a |
| <a name="provider_google-beta"></a> [google-beta](#provider\_google-beta) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [google-beta_google_firebase_project.default](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_firebase_project) | resource |
| [google_app_engine_application.app](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/app_engine_application) | resource |
| [google_project.project](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/project) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="firestore_region"></a> [firestore\_region](#input\_firestore\_region) | Firestore Region - must be app\_engine region | `string` | n/a | yes |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | GCP Project ID | `string` | `"aitutor-dev"` | no |
