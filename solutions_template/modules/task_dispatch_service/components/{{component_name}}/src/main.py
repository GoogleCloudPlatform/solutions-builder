"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
"""
  Tasks RESTful Microservice
"""
import uvicorn
import config
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from firedantic import configure
from google.cloud.firestore import Client

from routes import tasks

# Basic API config
service_title = "Tasks RESTful API"
service_path = "{{service_path}}"
version = "v1"

# Configurate Firestore and Firedantic
firestore_client = Client()
configure(firestore_client, prefix=config.DATABASE_PREFIX)

# Init FastAPI app
app = FastAPI(title=service_title)


@app.get("/ping")
def health_check():
  return True


@app.get("/", response_class=HTMLResponse)
@app.get(f"/{service_path}", response_class=HTMLResponse)
@app.get(f"/{service_path}/", response_class=HTMLResponse)
def hello():
  return f"You've reached the {service_title}: See <a href='/{service_path}/docs'>API docs</a>"


api = FastAPI(title=service_title, version=version)

# Append Tasks CRUD APIs to the app.
api.include_router(tasks.router)

app.mount(f"/{service_path}", api)

if __name__ == "__main__":
  uvicorn.run("main:app",
              host="0.0.0.0",
              port=int(config.PORT),
              log_level="info",
              reload=True)
