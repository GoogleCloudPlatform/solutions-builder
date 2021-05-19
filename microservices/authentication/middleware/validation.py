"""Utility methods for validating API request."""
import json
from os.path import join, dirname
import jsonschema
from jsonschema import validate


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

  def validate_data(*args, **kwargs):
    try:
      req = args[0].request
      method = req.method.lower()
      data = json.loads(req.body)

      uri_without_params = req.uri.split("?")[0]
      uri = [i for i in uri_without_params.split("/") if i]
      service = uri[0]
      if method == "post":
        schema = load_json_schema("{}_{}_schema.json".format(method, service))
      validate(data, schema)
      func(*args, **kwargs)
    except jsonschema.exceptions.ValidationError as err:
      args[0].send_json(success=False, status=400, message=str(err))

  return validate_data
