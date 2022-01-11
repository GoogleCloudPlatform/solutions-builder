terraform {
  backend "gcs" {
    bucket = "{{cookiecutter.project_id}}-tfstate"
    prefix = "env/dev"
  }
}
