"""
  Script to do portforwarding of different services.
"""
import yaml
import os
import subprocess
import argparse

# disabling for linting to pass
# pylint: disable = consider-using-with, subprocess-popen-preexec-fn

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--namespace", "-n")
  args = parser.parse_args()
  print("Setting up port-forward in namespace '%s'" % args.namespace)

  port_config_data = []
  with open("setup/port_config.yaml", "r", encoding="utf-8") as stream:
    port_config = yaml.safe_load(stream)
    port_config_data = port_config.get("data", [])

  for service in port_config_data:
    service_name = service.replace(".PORT", "")
    port = port_config_data[service]
    cmd = "kubectl port-forward service/%s %s:%s -n %s" % (service_name, port,
                                                           80, args.namespace)
    print(cmd)
    emulator = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
