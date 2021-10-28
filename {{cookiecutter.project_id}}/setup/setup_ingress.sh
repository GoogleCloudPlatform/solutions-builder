#!/bin/bash -e

# Example:
# PROJECT_ID=<GCP Project ID> \
#  EMAIL=jonchen@google.com \
#  WEB_APP_DOMAIN=<GCP Project ID>.cloudpssolutions.com \
#  API_DOMAIN=<GCP Project ID>-api.cloudpssolutions.com \
#  bash ./setup/setup_ingress.sh
#

declare -a EnvVars=(
  "PROJECT_ID"
  "WEB_APP_DOMAIN"
  "API_DOMAIN"
  "EMAIL"
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
echo "EMAIL=${EMAIL}"
echo "WEB_APP_DOMAIN=${WEB_APP_DOMAIN}"
echo "API_DOMAIN=${API_DOMAIN}"
echo


printf "\n${BLUE}Setting up kubectl to use context for project ${PROJECT_ID} ...${NORMAL}\n"
gcloud container clusters get-credentials default-cluster \
  --zone us-central1-a \
  --project $PROJECT_ID

printf "\n${BLUE}Setting up Cert manager ...${NORMAL}\n"
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.2.0/cert-manager.yaml
sed -i '' -e "s/_EMAIL_PLACEHOLDER/${EMAIL}/g" setup/certificate_issuer.yaml
kubectl apply -f setup/certificate_issuer.yaml
sed -i '' -e "s/${EMAIL}/_EMAIL_PLACEHOLDER/g" setup/certificate_issuer.yaml

printf "\n${BLUE}Setting up Nginx Ingress ...${NORMAL}\n"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.43.0/deploy/static/provider/cloud/deploy.yaml
sed -i '' -e "s/_WEB_APP_DOMAIN/${WEB_APP_DOMAIN}/g" setup/nginx_ingress.yaml
sed -i '' -e "s/_API_DOMAIN/${API_DOMAIN}/g" setup/nginx_ingress.yaml
kubectl apply -f setup/nginx_ingress.yaml
sed -i '' -e "s/${WEB_APP_DOMAIN}/_WEB_APP_DOMAIN/g" setup/nginx_ingress.yaml
sed -i '' -e "s/${API_DOMAIN}/_API_DOMAIN/g" setup/nginx_ingress.yaml

printf "\n${BLUE}Retrieving load balancer ingress IP address ...${NORMAL}\n"
INGRESS_IP_ADDRESS=""
while [[ "$INGRESS_IP_ADDRESS" = "" ]]; do
  INGRESS_IP_ADDRESS=`kubectl describe service/ingress-nginx-controller -n ingress-nginx | grep 'LoadBalancer Ingress:'`
  sleep 3
done

printf "\n${BLUE}Please create a DNS A record in https://domains.google.com/registrar/cloudpssolutions.com/dns to the following IP address: ${NORMAL}\n"
printf "API domain: https://$API_DOMAIN\n"
printf "${INGRESS_IP_ADDRESS}\n"
read -p  "${BLUE}Press any key to continue... \n ${NORMAL}" -n 1 -r

printf "\n${BLUE}Confirming the cert is issued correctly ...${NORMAL}\n"
SSL_VERIFY=`curl -v --silent https://${API_DOMAIN}/authentication/api/v1/validate 2>&1 | grep 'SSL certificate verify ok.'`
printf "$SSL_VERIFY\n"

if [[ "$SSL_VERIFY" = "" ]]; then
  printf "\n${RED}The API endpoint returns SSL issue. Please check the following URL in a browser manually: ${NORMAL}"
  printf "URL: https://${API_DOMAIN}/authentication/api/v1/validate \n"
  exit
fi

printf "\n${BLUE}Complete. ${NORMAL}\n"
