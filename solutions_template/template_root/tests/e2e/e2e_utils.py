import subprocess


def get_auth_identity_token():
  auth_token = exec_output("gcloud auth print-identity-token")
  return auth_token.replace("\n", "")


# Execute shell commands
def exec_shell(command, working_dir=".", stop_when_error=True, stdout=None):
  proc = subprocess.Popen(command, cwd=working_dir, shell=True, stdout=stdout)
  exit_status = proc.wait()

  if exit_status != 0 and stop_when_error:
    raise Exception(
        f"Error when running command: {command} (working_dir={working_dir})")

  return exit_status


# Execute shell commands
def exec_output(command, working_dir=".", stop_when_error=True):
  output = subprocess.check_output(command,
                                   cwd=working_dir,
                                   shell=True,
                                   text=True)
  return output
