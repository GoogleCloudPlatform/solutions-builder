terraform {
  backend "gcs" {
    # Uncomment below and specify a GCS bucket for TF state.
    # bucket = "PROJECT_ID-tfstate"
    prefix = "env/dev"
  }
}
