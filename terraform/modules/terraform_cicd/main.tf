module "cicd-terraform-account" {
  source       = "github.com/terraform-google-modules/cloud-foundation-fabric/modules/iam-service-account/"
  project_id   = var.project_id
  name         = "tf-${var.project_id}"
  display_name = "The Terraform Service Account. Used by CICD processes."

  # authoritative roles granted *on* the service accounts to other identities
  iam = {
    "roles/iam.serviceAccountUser" = []
  }
  # non-authoritative roles granted *to* the service accounts on other resources
  iam_project_roles = {
    (var.project_id) = [
      "roles/storage.admin",
      "roles/compute.instanceAdmin",
      "roles/iam.serviceAccountAdmin",
      "roles/secretmanager.admin",
      "roles/container.admin",
      "roles/iam.securityAdmin",
      "roles/compute.networkAdmin",
      "roles/appengine.appAdmin",
      "roles/dataflow.admin",
      # needed to create firestore
      # "roles/owner",
    ]
  }
}
