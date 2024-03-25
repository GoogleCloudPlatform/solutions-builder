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
import streamlit_google_oauth as oauth
from dotenv import load_dotenv

load_dotenv()
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
# redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]
redirect_uri = "http://localhost:8501"


def app():
  st.set_page_config(
      page_title="GenAI Solution",
      layout="wide",
      initial_sidebar_state="expanded",

  )

  st.title("Hello")

  login_info = oauth.login(
      client_id=client_id,
      client_secret=client_secret,
      redirect_uri=redirect_uri,
      # login_button_text="Continue with Google",
      logout_button_text="Logout",
  )
  if login_info:
    user_id, user_email = login_info
    st.write(f"Welcome {user_email}")
    st.switch_page("pages/Chat.py")

if __name__ == "__main__":
  app()
  logging.info("Streamlit main page rendered.")
