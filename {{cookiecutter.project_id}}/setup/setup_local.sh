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

CLUSTER_NAME=default-cluster
EXPECTED_CONTEXT=gke_${PROJECT_ID}_${REGION}_default-cluster

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
  gcloud container clusters get-credentials default-cluster --zone ${REGION} --project ${PROJECT_ID}
}

add_service_account_keys() {
  NAMESPACE=${SKAFFOLD_NAMESPACE}
  GSA_NAME="${PROJECT_ID}-sa"
  KSA_NAME="ksa"

  printf "\n${BLUE}Create Kubernetes Service Account to cluster ...${NORMAL}\n"
  declare EXISTING_KSA=`kubectl get sa -n ${NAMESPACE} | grep ${KSA_NAME}`
  if [[ "$EXISTING_KSA" = "" ]]; then
    kubectl create serviceaccount -n ${NAMESPACE} ${KSA_NAME}
  fi

  printf "\n${BLUE}Binding Kubernetes Service Account ${KSA_NAME} to GCP service account ${GSA_NAME} ...${NORMAL}\n"
  gcloud iam service-accounts add-iam-policy-binding \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:${PROJECT_ID}.svc.id.goog[${NAMESPACE}/${KSA_NAME}]" \
    ${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com

  printf "\n${BLUE}Adding service account annotation to ${KSA_NAME} ...${NORMAL}\n"
  kubectl annotate serviceaccount \
    --overwrite \
    --namespace ${NAMESPACE} \
    ${KSA_NAME} \
    iam.gke.io/gcp-service-account=${GSA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
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
