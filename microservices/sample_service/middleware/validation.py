"""Utility methods for validating API request."""
import json
from os.path import join, dirname
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def load_json_schema(schema_name):
  """
        Reads json file schema_name.json from specified directory
        and Returns it
        Args:
            schema_name: String
        Returns:
            schema_name.json: Json file
    """
  relative_path = join("schemas", schema_name)
  absolute_path = join(dirname(__file__), relative_path)

  with open(absolute_path) as schema_file:
    return json.loads(schema_file.read())


def validate_request(func):
  """
        This decorator function validates request body passed in API call
        against predefined json schema and Returns to calling function.
        Throws error if validation fails.
        Args:
            func
        Returns:
            func or raise error
    """

  async def validate_data(*args, **kwargs):
    try:
      req = args[0].request
      method = req.method.lower()
      if method in ["post", "put"]:
        data = json.loads(req.body)
      else:
        req_params = req.arguments
        for key in req_params:
          req_params[key] = req_params[key][0].decode("utf-8")
        data = req_params

      uri_without_params = req.uri.split("?")[0]
      uri = [i for i in uri_without_params.split("/") if i]
      service = uri[0]
      version = uri[2]
      if method in ["post", "get", "put"]:
        schema = load_json_schema("{}_{}_{}_schema.json".format(
            method, service, version))
      validate(data, schema)
      await func(*args, **kwargs)
    except ValidationError as err:
      return args[0].send_json(status=400, message=str(err), success=False)

  return validate_data
