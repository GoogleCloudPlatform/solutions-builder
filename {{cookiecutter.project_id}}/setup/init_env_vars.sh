export PROJECT_ID="{{cookiecutter.project_id}}"
export ADMIN_EMAIL="{{cookiecutter.admin_email}}"
export REGION={{cookiecutter.gcp_region}}
export API_DOMAIN={{cookiecutter.api_domain}}
export BASE_DIR=$(pwd)
export TF_VAR_project_id=${PROJECT_ID}
export TF_VAR_api_domain=${API_DOMAIN}
export TF_VAR_web_app_domain=${API_DOMAIN}
export TF_VAR_admin_email=${ADMIN_EMAIL}
export TF_BUCKET_NAME="${PROJECT_ID}-tfstate"
export TF_BUCKET_LOCATION="us"

# Terraform impersonate service account
export TF_RUNNER_SA_EMAIL="terraform-runner@$PROJECT_ID.iam.gserviceaccount.com"
export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=$TF_RUNNER_SA_EMAIL
