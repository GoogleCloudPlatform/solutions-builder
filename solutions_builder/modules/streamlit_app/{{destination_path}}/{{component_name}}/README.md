# Frontend Streamlit app

## Development

### Run streamlit locally

Set up API endpoint

```
# To unset environment variables:
unset AUTH_SERVICE_API_URL
unset LLM_SERVICE_API_URL
unset JOBS_SERVICE_API_URL

# Set API base URL
export API_BASE_URL=https://my.domain.com
```

Set the sub-path where the streamlit will deploy to. By default, it sets to "/streamlit"

```
export APP_BASE_PATH="/streamlit"
```

Install virtualenv and dependencies
```
python -m virtualenv .venv
source .venv/bin/activate
pip install -r components/common/requirements.txt
pip install -r components/frontend_streamlit/requirements.txt
```

```
PYTHONPATH=components/common/src streamlit run components/frontend_streamlit/src/main.py \
  --server.baseUrlPath=$APP_BASE_PATH
```

### Test local Streamlit with remote API, bypassing CORS

By default, browsers prevent cross-domain API calls from a web page/javascript, which includes calling a remote APIs from
the Streamlit UI hosted locally.

To bypass the CORS, run a Chrome browser instance separately with security setting disabled. Open a new terminal and run
commands below:

OSX:
```
open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome-user-data" --disable-web-security
```

Or on Windows:
```
"[PATH_TO_CHROME]\chrome.exe" --disable-web-security --disable-gpu --user-data-dir=~/chromeTemp
```

Once a new Chrome instance is up, copy and paste the Streamlit localhost and port.


### Run Streamlit locally with deployed microservices with local port forwording:

Build and deploy microservices with local port-forwording:

```
sb deploy -m authentication,llm_service,jobs_service -n $NAMESPACE --dev
```

Once deployed, it will show the corresponding services and ports like below:
```
Port forwarding service/authentication in namespace <namespace>, remote port 80 -> http://127.0.0.1:9001
Port forwarding service/llm-service in namespace <namespace>, remote port 80 -> http://127.0.0.1:9002
Port forwarding service/jobs-service in namespace <namespace>, remote port 80 -> http://127.0.0.1:9003
```
- Please note that the ports could be different when re-deploying. This is based on the skaffold.yaml
  in each microservice src folder.

Set the environment variables to override each API endpoints:
```
export AUTH_SERVICE_API_URL=http://127.0.0.1:9001/authentication/api/v1
export LLM_SERVICE_API_URL=http://127.0.0.1:9002/llm-service/api/v1
export JOBS_SERVICE_API_URL=http://127.0.0.1:9003/jobs-service/api/v1
```

Run Streamlit locally:
```
PYTHONPATH=components/common/src streamlit run components/frontend_streamlit/src/main.py \
  --server.baseUrlPath=$APP_BASE_PATH
```

### Deploy and run with livereload at remote GKE cluster

Deploy the microservice with livereload.
- This will run `skaffold dev` behind the scene.

```
sb deploy -n $NAMESPACE -m frontend_streamlit --dev
```

Once deployed successfully, you will see the output like below:
```
Deployments stabilized in 32.744 seconds
Port forwarding service/frontend-streamlit in namespace <namespace>, remote port 80 -> http://127.0.0.1:8080
```

At this point, the frontend app is ready and accessible at http://127.0.0.1:8080.

## Deployment

### Deploy to remote GKE cluster

Deploy the microservice.
- This will run `skaffold run` behind the scene.

```
sb deploy -n $NAMESPACE -m frontend_streamlit
```
