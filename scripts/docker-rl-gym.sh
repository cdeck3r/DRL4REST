#!/bin/bash

#
# Downloads the Dockerfile for the docker-rl-gym image 
# Source: https://github.com/jaimeps/docker-rl-gym
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
DOCKER_DIR="$PROJECT_DIR/Dockerfiles"

# Repo URL
REPO_URL="https://codeload.github.com/jaimeps/docker-rl-gym/zip/1204649d148a45c7cc56af71d2a95d3219f3ca11"

# include some common functions
# shellcheck source=/dev/null
source ./funcs.sh

#########################################
# option parsing
#########################################

usage() {
    echo -e "Usage: $0 [-h] [-d]"
    echo -e ""
    echo -e " h: this help text"
    echo -e " d: download dockerfiles"
}

DOWNLOAD_URL=0
PARAM_PARSE=0
while getopts "hd" opt; do
  PARAM_PARSE=1
  case ${opt} in
    d ) 
      DOWNLOAD_URL=1
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
    usage
    exit 0
fi

if [ $DOWNLOAD_URL -eq 1 ]; then
    log_echo "INFO" "Use the following params."
    log_echo "INFO" "REPO_URL: $REPO_URL"
    log_echo "INFO" "DOCKER_DIR: $DOCKER_DIR"
fi

#########################################
# Checks
#########################################

#
# Check other tools
log_echo "INFO" "Start checks ..."

if [ ! -d "${DOCKER_DIR}" ]; then
    log_echo "ERROR" "DOCKER_DIR does not exist. Abort."
    exit 1
fi

log_echo "INFO" "Checks done."

#########################################
#
# main program
#
#########################################

log_echo "INFO" "Download Dockerfiles"

rm -rf /tmp/docker-rl-gym
mkdir -p /tmp/docker-rl-gym
cd /tmp/docker-rl-gym || exit

curl ${REPO_URL} -o docker-rl-gym.zip || { 
  log_echo "ERROR" "Error downloading file: ${REPO_URL}"
  exit 1 
}

log_echo "INFO" "Move files to dir: ${DOCKER_DIR}"

# Unzip; cleanup; rename; mv all files to DOCKER_DIR
unzip -j docker-rl-gym.zip && rm docker-rl-gym.zip
rm README.md
mv Dockerfile Dockerfile.rlgym
mv ./* "${DOCKER_DIR}" 