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

def send_chat(prompt, chat_session_id=None):
  url = f"{API_BASE_URL}/chat/send_message"
  auth_token = st.session_state.token["id_token"]
  headers = {"Authorization": f"Bearer {auth_token}"}
  data = {
    "chat_session_id": chat_session_id,
    "prompt": prompt
  }
  return requests.post(
      url, headers=headers, json=data, timeout=30).json()


def get_chat_sessions():
  url = f"{API_BASE_URL}/chat/get_chat_sessions"
  auth_token = st.session_state.token["id_token"]
  headers = {"Authorization": f"Bearer {auth_token}"}
  resp_json = requests.get(url, headers=headers, timeout=30).json()
  return resp_json.get("chat_sessions", [])


def get_chat_messages(chat_session_id=None):
  if not chat_session_id:
    return []

  url = f"{API_BASE_URL}/chat/chat_session/{chat_session_id}"
  auth_token = st.session_state.token["id_token"]
  headers = {"Authorization": f"Bearer {auth_token}"}
  resp_json = requests.get(url, headers=headers, timeout=30).json()
  chat_session = resp_json.get("chat_session", None)

  # Get message history from a chat session.
  if not chat_session:
    return []

  messages = []
  for item in chat_session["history"]:
    messages.append({
        "role": "assistant" if item["role"] == "model" else item["role"],
        "content": item["parts"][0].get("text", "")
    })
  return messages


# Main content of the Chat page.
if __name__ == "__main__":
  if "token" not in st.session_state:
    st.switch_page("main.py")

  # Get chat session id from query params.
  st.session_state.chat_session_id = st.query_params.get("chat_session_id")
  print(st.session_state.chat_session_id)

  st.session_state.messages = get_chat_messages(
      st.session_state.chat_session_id)

  # Render side bar with existing chat sessions.
  with st.sidebar:
    if st.button("New session"):
      st.session_state.chat_session_id = None
      st.session_state.messages = []
      st.query_params.clear()

    st.subheader("Previous sessions")
    with st.spinner("Loading chat sessions..."):
      chat_sessions = get_chat_sessions()
      for chat_session in chat_sessions:
        # When clicked the chat session, switch with the history of the session.
        if st.button(f"- {chat_session['id']}"):
          st.session_state.chat_session_id = chat_session["id"]
          st.session_state.messages = get_chat_messages(chat_session["id"])
          st.query_params["chat_session_id"] = chat_session["id"]

  # Render chat page.
  st.title("Chat")
  if st.session_state.chat_session_id:
    st.write(f"Chat session ID: {st.session_state.chat_session_id}")

  else:
    # Initialize chat history
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! How can I help you today?"
    }]

  # Display chat messages from history on app rerun
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Accept user input
  if prompt := st.chat_input("Ask me anything."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      with st.spinner(""):
        result = send_chat(
            prompt=prompt,
            chat_session_id=st.session_state.get("chat_session_id"))

        st.session_state.chat_session_id = result["chat_session_id"]
        st.session_state.messages.append({
          "role": "assistant",
          "content": result["response"]})

        st.write(result["response"])
        st.query_params["chat_session_id"] = result["chat_session_id"]
