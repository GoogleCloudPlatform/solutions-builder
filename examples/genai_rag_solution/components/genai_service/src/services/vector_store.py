"""
Copyright 2023 Google LLC

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
# pylint: disable = broad-exception-raised, broad-exception-caught

import os
import gcsfs
from google.cloud import aiplatform
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders import GCSFileLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

PROJECT_ID = os.getenv("PROJECT_ID")
GCP_REGION = os.getenv("GCP_REGION")
DIMENSIONS = 768
DISPLAY_NAME = "vector_store"
ENDPOINT = "us-central1-aiplatform.googleapis.com"

# Initialize the client that will be used to create and send requests.
# This client only needs to be created once, and can be reused for multiple requests.
aiplatform.init(project=PROJECT_ID, location=GCP_REGION)


def load_pdf_file(gcs_path):
  documents = []
  fs = gcsfs.GCSFileSystem()
  files = fs.ls(gcs_path)

  # Print the files
  for filepath in files:
    bucket = filepath.split("/")[0]
    blobpath = "".join(filepath.split("/")[1:])
    loader = GCSFileLoader(
        project_name=PROJECT_ID,
        bucket=bucket,
        blob=blobpath,
        loader_func=PyPDFLoader
    )
    # load the document and split it into chunks
    documents += loader.load()

  return documents


def build_chroma_vector_store(documents, embedding_model="all-MiniLM-L6-v2"):
  assert PROJECT_ID, "PROJECT_ID environment variable must be set"
  assert GCP_REGION, "GCP_REGION environment variable must be set"

  # create the open-source embedding function
  embedding_function = SentenceTransformerEmbeddings(
      model_name=embedding_model)

  # load it into Chroma
  vectorstore = Chroma.from_documents(documents, embedding_function)

  return vectorstore
