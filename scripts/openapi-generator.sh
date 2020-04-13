#!/bin/bash

#
# Run the openapi generator application.
# It generates API for
# * python
# * python-flask
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
PROJECT_DIR=$(readlink -e "${SCRIPT_DIR}"/..)
OPENAPI_DIR="$PROJECT_DIR/openapi"

# Default API generation parameters
API_SPEC_URL="https://raw.githubusercontent.com/APIs-guru/openapi-directory/master/APIs/wmata.com/rail-station/1.0/swagger.yaml"
API_NAME=rail

# Image parameter initialization
IMG_NAME="openapitools/openapi-generator-cli"
TARGET=latest
IMAGE="${IMG_NAME}:${TARGET}"

# include some common functions
# shellcheck source=/dev/null
source ./funcs.sh

#########################################
# option parsing
#########################################

usage() {
    echo -e "Usage : $0 [-h] [-a] [-n]"
}

PARAM_PARSE=0
while getopts "ha:n:" opt; do
  PARAM_PARSE=1
  case ${opt} in
    a ) 
      API_SPEC_URL=$OPTARG
      ;;
    n ) 
      API_NAME=$OPTARG
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
    log_echo "INFO" "No params given. Use default params."
    log_echo "INFO" "API_SPEC_URL: $API_SPEC_URL"
    log_echo "INFO" "API_NAME: $API_NAME"
fi

#########################################
# Checks
#########################################

#
# Check other tools
log_echo "INFO" "Start checks ..."

if [ ! -d "${OPENAPI_DIR}" ]; then
    log_echo "WARN" "OPENAPI_DIR does not exist. Create dir: ${OPENAPI_DIR}"
    mkdir -p "${OPENAPI_DIR}"
fi

if [ ! -d "${OPENAPI_DIR}/${API_NAME}" ]; then
    log_echo "WARN" "API_NAME directory does not exist. Create dir: ${API_NAME}"
    mkdir -p "${OPENAPI_DIR}/${API_NAME}"
else
    log_echo "INFO" "Delete API_NAME content: ${OPENAPI_DIR}/${API_NAME}"
    rm -rf "${OPENAPI_DIR}/${API_NAME:?}/"*
fi


log_echo "INFO" "Checks done."

#########################################
#
# main program
#
#########################################

log_echo "INFO" "Start generating API code"

CODE_GENERATORS=( "python" "python-flask" )

for CODE_GEN in "${CODE_GENERATORS[@]}"
do
    log_echo "INFO" "Generate API for: $CODE_GEN in /local/${API_NAME}/${CODE_GEN}"

    docker run --rm \
        -v "${OPENAPI_DIR}":/local \
        $IMAGE generate \
        --input-spec "${API_SPEC_URL}" \
        --generator-name ${CODE_GEN} \
        --output /local/"${API_NAME}"/"${CODE_GEN}"
done
