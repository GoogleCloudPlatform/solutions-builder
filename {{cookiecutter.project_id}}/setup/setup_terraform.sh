declare -a EnvVars=(
  "PROJECT_ID"
)
for variable in ${EnvVars[@]}; do
  if [[ -z "${!variable}" ]]; then
    input_value=""
    while [[ -z "$input_value" ]]; do
      read -p "Enter the value for ${variable}: " input_value
      declare "${variable}=$input_value"
    done
  fi
done

BLUE=$(tput setaf 4)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)

create_bucket () {
  if [[ -z "${!TF_BUCKET_NAME}" ]]; then
    TF_BUCKET_NAME="${PROJECT_ID}-tfstate"
  fi

  if [[ -z "${!TF_BUCKET_LOCATION}" ]]; then
    TF_BUCKET_LOCATION="us"
  fi

  printf "PROJECT_ID=${PROJECT_ID}\n"
  printf "TF_BUCKET_NAME=${TF_BUCKET_NAME}\n"
  printf "TF_BUCKET_LOCATION=${TF_BUCKET_LOCATION}\n"

  print_highlight "Creating terraform state bucket: ${TF_BUCKET_NAME}.\n"
  gsutil mb -l $TF_BUCKET_LOCATION gs://$TF_BUCKET_NAME
  gsutil versioning set on gs://$TF_BUCKET_NAME
}

enable_apis () {
  gcloud services enable iamcredentials.googleapis.com
}

print_highlight () {
  printf "${BLUE}$1${NORMAL}\n"
}

create_bucket
enable_apis

echo
printf "Terraform state bucket: ${TF_BUCKET_NAME}\n"
