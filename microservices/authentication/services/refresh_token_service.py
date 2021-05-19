"""Utility method for Token generation."""
import requests


def get_id_token(payload, api_key):
  """
            Calls Google API using refresh_token as payload to generate
            new Id Token
            Args:
                payload: Dict(Object)
                API_KEY: String
            Returns:
                Token Credentials: Dict(Object)
        """
  resp = requests.post(
      "https://securetoken.googleapis.com/v1/token",
      payload,
      headers={"Content-Type": "application/x-www-form-urlencoded"},
      params={"key": api_key})
  return resp.json()
