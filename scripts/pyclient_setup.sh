#!/bin/bash

#
# Setup a given openapi python client 
#
# Author: cdeck3r
#

# this directory is the script directory
SCRIPT_DIR="$(
    cd "$(dirname "$0")" || exit
    pwd -P
)"
cd "$SCRIPT_DIR" || exit
# shellcheck disable=SC2034
SCRIPT_NAME=$0

# some variables
PROJECT_DIR=$(readlink -f "${SCRIPT_DIR}"/..)
OPENAPI_CLIENT_DIR="$PROJECT_DIR/openapi/cartpole/python"

# include some common functions
# shellcheck source=/dev/null
source ./funcs.sh

#########################################
# option parsing
#########################################

usage() {
    echo -e "Usage: $0 [-h] [-c]"
    echo -e ""
    echo -e "Options:"
    echo -e " h: this help text"
    echo -e " c: client dir"
}

PARAM_PARSE=0
while getopts "hc:" opt; do
  PARAM_PARSE=1
  case ${opt} in
    c ) 
      OPENAPI_CLIENT_DIR=$OPTARG
      ;;
    h ) usage
        exit 0
      ;;
    * )
       usage 
       exit 1
       ;;
  esac
done
shift $((OPTIND -1))

if [ $PARAM_PARSE -eq 0 ]; then
    log_echo "INFO" "Use the default  params."
    log_echo "INFO" "OPENAPI client dir: $OPENAPI_CLIENT_DIR"
fi

#########################################
# Checks
#########################################

#
# Check other tools
log_echo "INFO" "Start checks ..."

# check docker
# we expect the script to execute within the docker container
check_docker

if [ ! -d "${OPENAPI_CLIENT_DIR}" ]; then
    log_echo "ERROR" "OPENAPI client dir does not exist. Abort."
    exit 1
fi

log_echo "INFO" "Checks done."

#########################################
#
# main program
#
#########################################

log_echo "INFO" "Setup client"

cd "$OPENAPI_CLIENT_DIR" || exit

log_echo "INFO" "Install requirements"
pip3 install --no-cache-dir -r requirements.txt || exit

log_echo "INFO" "Setup client"
python setup.py install || exit