#!/bin/bash

#
# Setup a given openapi python-flask server 
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
OPENAPI_SERVER_DIR="$PROJECT_DIR/openapi/thenounproject/python-flask"


# include some common functions
# shellcheck source=/dev/null
source ./funcs.sh

#########################################
# option parsing
#########################################

usage() {
    echo -e "Usage: $0 [-h] [-s]"
    echo -e ""
    echo -e "Options:"
    echo -e " h: this help text"
    echo -e " s: server dir"
}

PARAM_PARSE=0
while getopts "hs:" opt; do
  PARAM_PARSE=1
  case ${opt} in
    s ) 
      OPENAPI_SERVER_DIR=$OPTARG
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
    log_echo "INFO" "OPENAPI client dir: $OPENAPI_SERVER_DIR"
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

if [ ! -d "${OPENAPI_SERVER_DIR}" ]; then
    log_echo "ERROR" "OPENAPI server dir does not exist. Abort."
    exit 1
fi

log_echo "INFO" "Checks done."

#########################################
#
# main program
#
#########################################

log_echo "INFO" "Setup client"

cd "$OPENAPI_SERVER_DIR" || exit

log_echo "INFO" "Install requirements"
pip3 install -r requirements.txt || exit

log_echo "INFO" "Start server"
export PYTHONPATH=${PROJECT_DIR}/src
python3 -m openapi_server
