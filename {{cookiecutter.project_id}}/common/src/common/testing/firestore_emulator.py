"""
  Pytest Fixture for getting firestore emulator
"""
import os
import signal
import subprocess
import time
import requests
import pytest

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import platform


# recreate the emulator each module - could consider changing to session
# pylint: disable = consider-using-with, subprocess-popen-preexec-fn
@pytest.fixture
def firestore_emulator():

  is_windows = bool(platform.system() == "Windows")
  if is_windows:
    emulator = subprocess.Popen(
        "firebase emulators:start --only firestore --project fake-project",
        shell=True)
  else:
    emulator = subprocess.Popen(
        "firebase emulators:start --only firestore --project fake-project",
        shell=True,
        preexec_fn=os.setsid)
  time.sleep(15)

  os.environ["FIRESTORE_EMULATOR_HOST"] = "{{cookiecutter.api_domain}}:8080"
  os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
  os.environ["PROJECT_ID"] = "fake-project"

  # yield so emulator isn't recreated each test
  yield emulator

  if is_windows:
    os.kill(emulator.pid, signal.CTRL_BREAK_EVENT)
  else:
    os.killpg(os.getpgid(emulator.pid), signal.SIGTERM)

  # delete debug files
  # some get deleted, not all

  try:
    os.remove("firestore-debug.log")
    os.remove("ui-debug.log")
  except OSError:
    pass

  # TODO: script to unset / reset the environmental variables
  # instead of just delete


# pylint: disable = line-too-long
@pytest.fixture
def clean_firestore(firestore_emulator):
  requests.delete(
      "http://{{cookiecutter.api_domain}}:8080/emulator/v1/projects/fake-project/databases/(default)/documents",
      timeout=10)
