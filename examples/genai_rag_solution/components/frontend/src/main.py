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
import logging
import os
import streamlit as st
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv

load_dotenv()

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]
SCOPE = "openid profile email"


def app():
  st.set_page_config(
      page_title="GenAI Solution",
      layout="wide",
      initial_sidebar_state="expanded",

  )

  st.title("Hello")

  # Streamlit component: https://github.com/dnplus/streamlit-oauth
  oauth2 = OAuth2Component(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
                           AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

  # Check if token exists in session state
  if "token" not in st.session_state:
    # If not, show authorize button
    result = oauth2.authorize_button(
        "Continue with Google", REDIRECT_URI, SCOPE)
    if result and "token" in result:
      # If authorization successful, save token in session state
      st.session_state.token = result.get("token")
      st.rerun()
  else:
    # If token exists in session state, navigate to Chat page.
    st.switch_page("pages/Chat.py")


if __name__ == "__main__":
  app()
  logging.info("Streamlit main page rendered.")
