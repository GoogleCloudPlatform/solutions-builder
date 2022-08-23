terraform {
  backend "gcs" {
    # Specify a GCS bucket for TF state.
    bucket = "{{cookiecutter.project_id}}-tfstate"
    prefix = "env/dev"
  }
}
