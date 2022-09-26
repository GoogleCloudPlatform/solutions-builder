#!/usr/bin/env bash
set -e



cli_help() {
  cli_name=${0##*/}
  echo "
$cli_name

Solutions Template - UnitTest Helper
Version: 1.0
Usage: $cli_name [action] [action_arg]
Actions:
  firebase_emulator
  install_dependencies
  run_pytest
  run_linter

Example:
  Install python Firebase Emulator:
  $ unittest_helper.sh firebase_emulator

  Install python dependencies with a specific folder:
  $ unittest_helper.sh install_dependencies <target-folder>

  Run pytest with a specific folder:
  $ unittest_helper.sh run_pytest <target-folder>
  "
  exit 1
}

### Install Firebase Emulator
install_firebase_emulator() {
  echo "Install Firebase CLI"
  curl -sL https://firebase.tools | bash
  
  echo "Download Firestore emulator"
  firebase setup:emulators:firestore
}

### Install all python dependencies
install_dependencies() {
  BASE_DIR=$(pwd)
  TARGET_FOLDER=$1
  assert TARGET_FOLDER "TARGET_FOLDER is not defined in <action_arg>"
  cd $TARGET_FOLDER
  
  python -m pip install --upgrade pip
  python -m pip install pytest pytest-custom_exit_code pytest-cov pylint pytest-mock mock
  if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
  if [ -f requirements-test.txt ]; then pip install -r requirements-test.txt; fi
  if [ -f $BASE_DIR/common/requirements.txt ]; then pip install -r $BASE_DIR/common/requirements.txt; fi
  
  cd $BASE_DIR
}

### Run unit test with Pytest with a specific folder.
run_pytest() {
  BASE_DIR=$(pwd)
  TARGET_FOLDER=$1
  assert TARGET_FOLDER "TARGET_FOLDER is not defined in <action_arg>"
  
  cd $TARGET_FOLDER
  PYTEST_ADDOPTS="--cache-clear --cov . " PYTHONPATH=$BASE_DIR/common/src python -m pytest src
  cd $BASE_DIR
}

### Run Linter with a specific folder.
run_linter() {
  BASE_DIR=$(pwd)
  TARGET_FOLDER=$1
  assert TARGET_FOLDER "TARGET_FOLDER is not defined in <action_arg>"
  
  cd $TARGET_FOLDER/src
  python -m pip install --upgrade pip
  python -m pip install pylint
  python -m pylint $(git ls-files '*.py') --rcfile=$BASE_DIR/.pylintrc
  cd $BASE_DIR
}

assert() {
  if [[ -z "${!1}" ]]; then
    echo $2
    exit 1
  fi
}

### Main switch case.

case "$1" in
  firebase_emulator)
    install_firebase_emulator
  ;;
  install_dependencies)
    install_dependencies $2
  ;;
  run_pytest)
    run_pytest $2
  ;;
  run_linter)
    run_linter $2
  ;;
  *)
    cli_help
  ;;
esac

