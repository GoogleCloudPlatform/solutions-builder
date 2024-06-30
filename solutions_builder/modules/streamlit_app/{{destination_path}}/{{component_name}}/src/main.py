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
import importlib
import logging
import streamlit as st


def render():
  st.set_page_config(
      page_title="{{streamlit_app_name}}",
      page_icon="💬",
      layout="wide",
      initial_sidebar_state="expanded",
  )
  with st.sidebar:
    st.title("{{streamlit_app_name}}")

  st.title("{{streamlit_app_name}}")
  st.divider()
  st.write("Add your content here.")


if __name__ == "__main__":
  render()
  logging.info("Streamlit main page rendered.")
