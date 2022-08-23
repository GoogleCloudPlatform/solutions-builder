GSA_NAME="gke-node-sa"
KSA_NAME="ksa"

declare EXISTING_KSA=`kubectl get sa -n ${NAMESPACE} | egrep -i "^${KSA_NAME} "`
if [[ "$EXISTING_KSA" = "" ]]; then
  kubectl create serviceaccount -n ${NAMESPACE} ${KSA_NAME}
fi

gcloud iam service-accounts add-iam-policy-binding \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:${GCP_PROJECT}.svc.id.goog[${NAMESPACE}/${KSA_NAME}]" \
  ${GSA_NAME}@${GCP_PROJECT}.iam.gserviceaccount.com

kubectl annotate serviceaccount \
  --overwrite \
  --namespace ${NAMESPACE} \
  ${KSA_NAME} \
  iam.gke.io/gcp-service-account=${GSA_NAME}@${GCP_PROJECT}.iam.gserviceaccount.com