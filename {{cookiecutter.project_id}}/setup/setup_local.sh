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

EXPECTED_CONTEXT=gke_${PROJECT_ID}_${REGION}_default-cluster

BLUE=$(tput setaf 4)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)
echo
echo "PROJECT_ID=${PROJECT_ID}"
echo "SKAFFOLD_NAMESPACE=${SKAFFOLD_NAMESPACE}"
echo

printf "\n${BLUE}Set up gcloud and kubectl context ...${NORMAL}\n"
gcloud container clusters get-credentials default-cluster --region ${REGION} --project ${PROJECT_ID}

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

printf "\n${BLUE}Adding Service Account to cluster ...${NORMAL}\n"
EXISTING_SECRET=`kubectl get secrets -n $SKAFFOLD_NAMESPACE | grep 'default-sa-key'`
if [[ "$EXISTING_SECRET" = "" ]]; then
  gcloud iam service-accounts keys create ./.tmp/$PROJECT_ID-sa-key.json \
  --iam-account=$PROJECT_ID-sa-dev@$PROJECT_ID.iam.gserviceaccount.com
  kubectl create secret generic default-sa-key --from-file=./.tmp/${PROJECT_ID}-sa-key.json
  rm ./.tmp/$PROJECT_ID-sa-key.json
else
  printf "Secret 'default-sa-key' already exists in the cluster (namespace: ${SKAFFOLD_NAMESPACE}).\n"
fi

printf "\n${BLUE}Done. ${NORMAL}\n"
