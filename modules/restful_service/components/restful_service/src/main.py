"""
  Todos RESTful Microservice
"""
import uvicorn
import config
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from firedantic import configure
from google.cloud.firestore import Client

from routes import todos

# Basic API config
service_title = "Todos RESTful API"
service_path = "restful_service"
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

# Append Todo CRUD APIs to the app.
api.include_router(todos.router)

app.mount(f"/{service_path}", api)

if __name__ == "__main__":
  uvicorn.run("main:app",
              host="0.0.0.0",
              port=int(config.PORT),
              log_level="info",
              reload=True)
