# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
  Streamlit app main file
"""
import os
import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:9002/genai-service")


def send_query(prompt):
  url = f"{API_BASE_URL}/query/send_query"
  auth_token = st.session_state.token["id_token"]
  headers = {"Authorization": f"Bearer {auth_token}"}
  data = {
    "query": prompt
  }
  return requests.post(
      url, headers=headers, json=data, timeout=30).json()


def print_source(sources):
  st.write("Sources:")
  for source in sources:
    source_uri = source["metadata"]["source"]
    page = source["metadata"]["page"]
    page_content = source["page_content"]
    st.markdown(f"""
    - Source Doc: [{source_uri}]() (Page {page})
      - {page_content}
    """)


# Main content of the Chat page.
if __name__ == "__main__":
  if "token" not in st.session_state:
    st.switch_page("main.py")

  # Render query page.
  st.title("Query")
  # Initialize chat history
  st.session_state.messages = [{
      "role": "assistant",
      "content": "Hello! How can I help you today?"
  }]

  # Display chat messages from history on app rerun
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

      if "sources" in message:
        print_source(message["sources"])

  # Accept user input
  if prompt := st.chat_input("Ask me anything."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      with st.spinner(""):
        result = send_query(prompt=prompt)

        st.session_state.messages.append({
          "role": "assistant",
          "content": result["response"],
          "sources": result["sources"],
        })

        st.write(result["response"])
        if "sources" in result:
          print_source(result["sources"])
