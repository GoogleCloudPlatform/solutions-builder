"""Utility methods for token validation."""
from config import COLLECTION
from services.firestore_service import insert_document, user_exist
from services.cache_service import set_key, get_key
from services.firebase_authentication import verify_token
from utils.logging_handler import Logger


def handle_user(decoded_token):
  """
          Checks for user_email in database, if found stores
          user_details in cache and Returns new_user = False,
          else inserts user name and email in database and in
          cache as well, Returns new_user = True
          Args:
              Decoded Token: Dict
          Returns:
              User Type: Dict
      """
  user_email = decoded_token["email"]
  user_name = decoded_token.get("name")
  user_id = decoded_token["user_id"]

  if user_exist(COLLECTION, user_email):
    user_details = {"new_user": False}
    cached_user = set_key(
        key="cache::{}".format(user_id),
        value={
            "email": user_email,
            "name": user_name
        })
  else:
    data = {"email": user_email, "name": user_name, "user_id": user_id}
    doc_status = insert_document(COLLECTION, data, user_id)
    cached_user = set_key("cache::{}".format(user_id), data)
    Logger.info(
        "Inserting new user into firestore status: {}".format(doc_status))
    Logger.info("Caching user Id in redis: {}".format(cached_user))
    user_details = {"new_user": True}
  return user_details


def validate_token(bearer_token):
  """
          Validates Token passed in headers, Returns user
          auth details along with user_type = new or old
          In case of Invalid token Throws error
          Args:
              Bearer Token: String
          Returns:
              Decoded Token and User type: Dict
      """
  token = bearer_token.split(" ")
  cached_token = get_key("cache::{}".format(token[1]))
  if cached_token is None:
    decoded_token = verify_token(token[1])
    cache_token = set_key("cache::{}".format(token[1]), decoded_token, 1800)
    Logger.info("Id Token caching status: {}".format(cache_token))
  else:
    decoded_token = cached_token

  cached_user = get_key("cache::{}".format(decoded_token["user_id"]))
  user_type = handle_user(decoded_token) if cached_user is None else {
      "new_user": False
  }
  return {**decoded_token, **user_type}
