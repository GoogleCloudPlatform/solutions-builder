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

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from vertexai.generative_models import GenerativeModel, Content
from common.utils.auth import verify_oauth2_token
from models.chat_session import ChatSession

# pylint: disable = broad-except

# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/chat", tags=["chat"])

SUCCESS_RESPONSE = {"status": "Success"}

model = GenerativeModel("gemini-1.0-pro")


def chat_history_to_list(chat_history: list):
  output = []
  for item in chat_history:
    output.append(item.to_dict())
  return output

def chat_history_to_contents(chat_history: list):
  output = []
  for item in chat_history:
    output.append(Content.from_dict(item))
  return output

# Get all chat sessions of a user.
@router.get("/get_chat_sessions")
async def get_chat_sessions(user_data: dict = Depends(verify_oauth2_token)):
  print(user_data)
  # Get previous chat session from this user.
  result = ChatSession.find_by_user(email=user_data["email"])
  chat_sessions = []
  for item in result:
    chat_sessions.append(item.to_dict())

  return {
    "chat_sessions": chat_sessions,
    "status": "Success",
  }


# Get a chat session by ID.
@router.get("/chat_session/{chat_session_id}")
async def get_chat_session(chat_session_id):
  chat_session = ChatSession.find_by_id(chat_session_id)
  print(f"chat_session: {chat_session}")

  return {
    "chat_session": chat_session,
    "status": "Success",
  }

# Send a chat message to model.
@router.post("/send_message")
async def send_message(
    data: dict, user_data: dict = Depends(verify_oauth2_token)):

  print(f"data: {data}")
  if "prompt" not in data:
    raise HTTPException(status_code=400, detail="Missing 'prompt' in data.")

  chat_history = []
  chat_session_id = data.get("chat_session_id")
  if chat_session_id:
    # Get chat session from database.
    chat_session = ChatSession.find_by_id(chat_session_id)
    if not chat_session:
      raise HTTPException(status_code=404, detail="Chat session not found.")

    chat_history = chat_session.history
  else:
    # Create a new chat session.
    chat_session = ChatSession(email=user_data["email"])
    chat_session.save()

  # Start a chat session.
  chat = model.start_chat(history=chat_history_to_contents(chat_history))
  response = chat.send_message(data["prompt"])

  # Save chat history to ChatSession object in Firestore.
  chat_history = chat_history_to_list(chat.history)
  chat_session.history = chat_history
  chat_session.save()

  # Return the response.
  print(f"response: {response}")

  return {
    "chat_session_id": chat_session.id,
    "response": response.text,
    "status": "Success",
  }
