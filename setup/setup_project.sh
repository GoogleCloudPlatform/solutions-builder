#!/bin/bash -e

replace_var () {
  old_value=$1
  new_value=$2
  filename=$3
  sed -i '' -e "s/${old_value}/${new_value}/g" ${filename}
}

restore_var () {
  old_value=$1
  new_value=$2
  filename=$3
  sed -i '' -e "s/${new_value}/${old_value}/g" ${filename}
}

declare -a EnvVars=(
  "PROJECT_ID"
  "REGION"
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

init () {
  export BUCKET_NAME=$PROJECT_ID-tfstate
  export BUCKET_LOCATION=us

  # gcloud auth application-default login
  gcloud config set project $PROJECT_ID

  { # try
    printf "\n${BLUE}Creating bucket $BUCKET_NAME ...${NORMAL}\n"
    gsutil mb -l $BUCKET_LOCATION gs://$BUCKET_NAME
  } || { # catch
    echo
  }

  gsutil versioning set on gs://$BUCKET_NAME
}

run_terraform () {
  printf "\n${BLUE}Preparing to run Terraform ...${NORMAL}\n"
  export TF_VAR_project_id=$PROJECT_ID
  export TF_VAR_region=$REGION

  cd terraform/environments/dev
  terraform init -backend-config="bucket=$BUCKET_NAME"
  terraform plan

  prompt_continue "${BLUE}Do you want to perform these Terraform actions? (y/n) ${NORMAL}"
  terraform apply -auto-approve
}

print_complete() {
  printf "\n${BLUE}Complete.${NORMAL}\n"
}

prompt_continue() {
  read -p "$1" -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
  else
    printf "\nTerminated.\n"
    exit 0
  fi
}

echo
prompt_continue "${BLUE}This will set up project \"$PROJECT_ID\" in \"$REGION\". Continue? (y/n) ${NORMAL}"
init
run_terraform
print_complete