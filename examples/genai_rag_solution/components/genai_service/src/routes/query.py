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
import os
import uuid
from fastapi import APIRouter, Depends
from langchain.storage import InMemoryStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from langchain_core.documents import Document
from langchain.retrievers.multi_vector import MultiVectorRetriever

from common.utils.auth import verify_oauth2_token
from services.vector_store import build_chroma_vector_store, load_pdf_file


router = APIRouter(prefix="/query", tags=["query"])

SUCCESS_RESPONSE = {"status": "Success"}
DOCS_GCS_BUCKET = os.getenv("DOCS_GCS_BUCKET")
PROJECT_ID = os.getenv("PROJECT_ID")

assert PROJECT_ID, f"PROJECT_ID is not set"
assert DOCS_GCS_BUCKET, f"DOCS_GCS_BUCKET is not set"


def create_retriever_multi_vector(gcs_bucket_path, id_key="doc_id"):
  docstore = InMemoryStore()

  # Create a vector store using local Chroma instance.
  documents = load_pdf_file(gcs_bucket_path)
  vector_store = build_chroma_vector_store(documents)

  # Create the multi-vector retriever
  retriever = MultiVectorRetriever(
      vectorstore=vector_store,
      docstore=docstore,
      id_key=id_key,
  )

  # Add documents to the retriever.
  doc_ids = [str(uuid.uuid4()) for _ in documents]
  all_docs = [
      Document(page_content=s.page_content, metadata={id_key: doc_ids[i]})
      for i, s in enumerate(documents)
  ]

  retriever.docstore.mset(list(zip(doc_ids, documents)))
  retriever.vectorstore.add_documents(all_docs)
  return retriever


retriever = create_retriever_multi_vector(
    DOCS_GCS_BUCKET)


@router.post("/send_query")
async def send_query(
        data: dict, user_data: dict = Depends(verify_oauth2_token)):

  # Create prompt.
  template = """
  Answer the question based only on the following context:
  {context}

  Question: {question}
  """
  prompt = ChatPromptTemplate.from_template(template)

  # Create RAG chain
  rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | ChatVertexAI(
        temperature=user_data.get("temperature", 0),
        model_name=user_data.get("model_name", "gemini-pro-vision"),
        max_output_tokens=1024
    )  # Multi-modal LLM
    | StrOutputParser()
  )

  query = data["query"]
  result = rag_chain.invoke(query)
  docs = retriever.get_relevant_documents(query, limit=10)

  return {
      "status": "success",
      "response": result,
      "sources": docs,
  }
