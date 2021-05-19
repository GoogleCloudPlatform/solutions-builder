#!/bin/bash -e

# Example:
# PROJECT_ID=<GCP Project ID> bash ./setup/setup_cluster.sh

# Default paths for ML models and demo firestore collection.
ML_STORAGE_PROJECT=solutions-template
ML_BUCKET=solutions-template.appspot.com
CLUSTER_NAME=default-cluster
FIRESTORE_DEMO_PATH=gs://solutions-template.appspot.com/collection_export_2021-03-03

declare -a EnvVars=(
  "PROJECT_ID"
)
for variable in ${EnvVars[@]}; do
  if [[ -z "${!variable}" ]]; then
    printf "$variable is not set.\n"
    exit -1
  fi
done
BLUE=$(tput setaf 4)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)
echo
echo "PROJECT_ID=${PROJECT_ID}"
echo "CLUSTER_NAME=${CLUSTER_NAME}"
echo "ML_STORAGE_PROJECT=${ML_STORAGE_PROJECT}"
echo "ML_BUCKET=${ML_BUCKET}"
echo "FIRESTORE_DEMO_PATH=${FIRESTORE_DEMO_PATH}"
echo

read -p  "${BLUE}This will set up the GKE cluster \"$CLUSTER_NAME\" in project \"$PROJECT_ID\". Continue? (y/n) ${NORMAL}" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo
else
  printf "\nTerminated.\n"
  exit 0
fi

printf "\n${BLUE}Checking if GCP project ${PROJECT_ID} exists... ${NORMAL}\n"
EXISTING_PROJECT_ID=`gcloud projects list --filter ${PROJECT_ID} | grep ${PROJECT_ID}`
if [[ "$EXISTING_PROJECT_ID" == "" ]]; then
  printf "Project ${PROJECT_ID} doesn't exist or you don't have access.\n"
  printf "Terminated.\n"
  exit 0
else
  printf "Project ${PROJECT_ID} found.\n"
fi

printf "\n${BLUE}Switch gcloud config to project ${PROJECT_ID} ${NORMAL}\n"
gcloud config set project $PROJECT_ID

printf "\n${BLUE}Enabling services for project ${PROJECT_ID} ...${NORMAL}\n"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable firebase.googleapis.com
gcloud services enable firestore.googleapis.com

printf "\n${BLUE}Creating cluster ${CLUSTER_NAME} in project ${PROJECT_ID} ... ${NORMAL}\n"
EXISTING_CLUSTER_ID=`gcloud container clusters list | grep "$CLUSTER_NAME"`
if [[ "$EXISTING_CLUSTER_ID" = "" ]]; then
  gcloud container clusters create $CLUSTER_NAME \
    --machine-type=n1-highmem-2 \
    --scopes=cloud-platform \
    --enable-autoscaling \
    --min-nodes=2 \
    --max-nodes=10 \
    --zone=us-central1-a

  ### Uncomment this to enable GPU nodes.
  # gcloud container node-pools create deeplit-nodes-gpu-dev \
  #   --cluster $CLUSTER_NAME \
  #   --num-nodes 1 \
  #   --machine-type=n1-highmem-2 \
  #   --accelerator type=nvidia-tesla-t4,count=1 \
  #   --scopes=cloud-platform \
  #   --enable-autoscaling \
  #   --min-nodes=1 \
  #   --max-nodes=5 \
  #   --zone=us-central1-a \
  #   --node-taints key=gpu:NoSchedule
else
  printf "Cluster $CLUSTER_NAME already exists in project ${PROJECT_ID}\n"
fi

printf "\n${BLUE}Setting up kubectl to use context for project ${PROJECT_ID} ...${NORMAL}\n"
gcloud container clusters get-credentials $CLUSTER_NAME \
  --zone us-central1-a \
  --project $PROJECT_ID

printf "\n${BLUE}Setting up GKE Port config ...${NORMAL}\n"
kubectl apply -f ./setup/port_config.yaml


printf "\n${BLUE}Adding Service Account to cluster ...${NORMAL}\n"
EXISTING_SECRET=`kubectl get secrets | grep 'default-sa-key'`
if [[ "$EXISTING_SECRET" = "" ]]; then
  PROJECT_NUMBER=$(gcloud projects list --filter="$PROJECT_ID" --format="value(PROJECT_NUMBER)")
  gcloud iam service-accounts keys create ./.tmp/$PROJECT_ID.json \
  --iam-account ${PROJECT_NUMBER}-compute@developer.gserviceaccount.com
  kubectl create secret generic default-sa-key --from-file=./.tmp/${PROJECT_ID}.json
  rm ./.tmp/$PROJECT_ID.json
else
  printf "Secret default-sa-key already exists in the cluster (namespace: default).\n"
fi

printf "\n${BLUE}Retriving Helm and Redis... ${NORMAL}\n"
cd .tmp
curl https://get.helm.sh/helm-v3.5.2-darwin-amd64.tar.gz -O
tar -xzvf helm-v3.5.2-darwin-amd64.tar.gz
printf "\n${BLUE}Copying Helm to /usr/local/bin/helm. You may need to enter sudo password. ${NORMAL}\n"
sudo mv darwin-amd64/helm /usr/local/bin/helm
rm -rf darwin-amd64
cd ..

printf "\n${BLUE}Installing bitnami... ${NORMAL}\n"
helm repo add bitnami https://charts.bitnami.com/bitnami

printf "\n${BLUE}Installing bitnami/redis... ${NORMAL}\n"
EXISTING_REDIS=`helm list | grep redis`
if [[ "$EXISTING_REDIS" = "" ]]; then
  helm install redis bitnami/redis --set usePassword=false
else
  printf "Redis already exists in namespace=caching ${PROJECT_ID}\n"
fi

printf "\n${BLUE}Complete. ${NORMAL}\n"
