# Hardcoded the project ID for all local development.
declare -a EnvVars=(
  "PROJECT_ID"
  "SKAFFOLD_NAMESPACE"
  "REGION"
)
for variable in ${EnvVars[@]}; do
  if [[ -z "${!variable}" ]]; then
    printf "$variable is not set.\n"
    exit -1
  fi
done

CLUSTER_NAME=main-cluster
EXPECTED_CONTEXT=gke_${PROJECT_ID}_${REGION}_main-cluster

BLUE=$(tput setaf 4)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)
echo
echo "PROJECT_ID=${PROJECT_ID}"
echo "SKAFFOLD_NAMESPACE=${SKAFFOLD_NAMESPACE}"
echo "REGION=${REGION}"
echo


init() {
  printf "\n${BLUE}Switch gcloud config to project ${PROJECT_ID} ${NORMAL}\n"
  EXISTING_PROJECT_ID=`gcloud projects list --filter ${PROJECT_ID} | grep ${PROJECT_ID}`
  if [[ "$EXISTING_PROJECT_ID" == "" ]]; then
    printf "Project ${PROJECT_ID} doesn't exist or you don't have access.\n"
    printf "Terminated.\n"
    exit 0
  else
    printf "Project ${PROJECT_ID} found.\n"
  fi

  gcloud config set project $PROJECT_ID

  printf "\n${BLUE}Set up gcloud and kubectl context ...${NORMAL}\n"
  gcloud container clusters get-credentials main-cluster --zone ${REGION} --project ${PROJECT_ID}
}

setup_namespace() {
  printf "\n${BLUE}Creating namespace: ${SKAFFOLD_NAMESPACE} ...${NORMAL}\n"
  kubectl create ns $SKAFFOLD_NAMESPACE

  printf "\n${BLUE}Using namespace ${SKAFFOLD_NAMESPACE} for all kubectl operations ...${NORMAL}\n"
  kubectl config set-context --current --namespace=$SKAFFOLD_NAMESPACE

  printf "\n${BLUE}Verifying the kubectl context name ...${NORMAL}\n"
  CURRENT_CONTEXT=`kubectl config current-context`
  if [[ "$CURRENT_CONTEXT" = "$EXPECTED_CONTEXT" ]]; then
    printf "OK.\n"
  else
    printf "${RED}Expecting kubectl context as "${EXPECTED_CONTEXT}" but got "${CURRENT_CONTEXT}". ${NORMAL}\n"
  fi
}

read -p  "${BLUE}This will set up for local development using namespace \
\"${SKAFFOLD_NAMESPACE}\" in \"$CLUSTER_NAME\" in project \"$PROJECT_ID\". \
Continue? (y/n) ${NORMAL}" -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo
else
  printf "\nTerminated.\n"
  exit 0
fi

init
add_service_account_keys
setup_namespace

printf "\n${BLUE}Done. ${NORMAL}\n"
