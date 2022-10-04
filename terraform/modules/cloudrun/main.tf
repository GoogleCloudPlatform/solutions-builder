locals {
  allow_unauthenticated_flag = (var.allow_unauthenticated ? "--allow-unauthenticated" : "")
}

resource "google_artifact_registry_repository" "cloudrun_repository" {
  location      = var.region
  repository_id = var.repository_id
  description   = "Docker repository for CloudRun"
  format        = "DOCKER"
}

resource "google_cloud_run_service_iam_member" "member" {
  count    = (var.allow_unauthenticated ? 1 : 0)
  project  = var.project_id
  location = var.region
  service  = var.service_name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Creating a custom service account for cloud run
module "cloud-run-service-account" {
  source       = "github.com/terraform-google-modules/cloud-foundation-fabric/modules/iam-service-account/"
  project_id   = var.project_id
  name         = "cloudrun-sa"
  display_name = "This is service account for cloud run"

  iam = {
    "roles/iam.serviceAccountUser" = []
  }

  iam_project_roles = {
    (var.project_id) = [
      "roles/eventarc.eventReceiver",
      "roles/firebase.admin",
      "roles/firestore.serviceAgent",
      "roles/iam.serviceAccountUser",
      "roles/iam.serviceAccountTokenCreator",
      "roles/run.invoker",
      "roles/pubsub.serviceAgent",
    ]
  }
}

# Build common image
data "archive_file" "common-zip" {
  type        = "zip"
  source_dir  = "../../../common"
  output_path = ".terraform/common.zip"
}
resource "null_resource" "build-common-image" {
  triggers = {
    src_hash = "${data.archive_file.cloudrun-zip.output_sha}"
  }
  provisioner "local-exec" {
    working_dir = "../../../common"
    command = join(" ", [
      "gcloud builds submit",
      "--config=cloudbuild.yaml",
      join("", [
        "--substitutions=",
        join(",", [
          "_PROJECT_ID='${var.project_id}'",
          "_IMAGE='common'",
          "_REGION='${var.region}'",
          "_REPOSITORY=${var.repository_id}",
        ])
      ])
    ])
  }
}

# Build Cloudrun image
data "archive_file" "cloudrun-zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = ".terraform/${var.service_name}.zip"
}
resource "null_resource" "deploy-cloudrun-image" {
  depends_on = [
    null_resource.build-common-image
  ]
  triggers = {
    src_hash = "${data.archive_file.cloudrun-zip.output_sha}"
  }
  provisioner "local-exec" {
    working_dir = var.source_dir
    command = join(" ", [
      "gcloud builds submit",
      "--config=cloudbuild.yaml",
      join("", [
        "--substitutions=",
        join(",", [
          "_PROJECT_ID='${var.project_id}'",
          "_IMAGE='queue-image'",
          "_REGION='${var.region}'",
          "_REPOSITORY=${var.repository_id}",
          "_SERVICE_ACCOUNT='${module.cloud-run-service-account.email}'",
          "_CLOUD_RUN_SERVICE_NAME='${var.service_name}'",
          "_ALLOW_UNAUTHENTICATED_FLAG='${local.allow_unauthenticated_flag}'"
        ])
      ])
    ])
  }
}
