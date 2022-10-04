import yaml

port_config_data = []
with open("setup/port_config.yaml", "r") as stream:
  port_config = yaml.safe_load(stream)
  port_config_data = port_config.get("data", [])


def get_baseurl(service_name):
  port = port_config_data[service_name + ".PORT"].split(":")[0]
  return f"http://localhost:{port}"

