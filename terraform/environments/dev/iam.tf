locals {
  # TODO: Add users to your project below.
  role_members = {
    admin = [
      # "user:admin@example.com",
    ]
    breakglass = [
      # "user:admin@example.com",
    ]
    editor = [
      # "user:developer@example.com",
    ]
    viewer = [
      # "user:developer@example.com",
    ]
  }
}

# Additive IAM bindings. Must not conflict with authoritative bindings below.
module "projects_iam_bindings" {
  source  = "terraform-google-modules/iam/google//modules/projects_iam"
  version = "7.4.1"

  projects = [var.project_id]
  mode     = "additive"

  bindings = {
    "roles/owner" = flatten([
      local.role_members.admin,
    ])
    "roles/editor" = flatten([
      local.role_members.breakglass,
      local.role_members.editor,
    ])
    "roles/viewer" = flatten([
      local.role_members.viewer
    ])
    "roles/resourcemanager.projectIamAdmin" = flatten([
      local.role_members.breakglass,
      local.role_members.admin,
    ])
  }
}
