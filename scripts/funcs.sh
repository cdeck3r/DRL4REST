#!/bin/bash

#
# Common funcs for scripts
# to be sourced in various scripts
#
# Author: cdeck3r
#

# reads and exports all env vars, mostly tokens
if [ -f $HOME/.env ]; then
	export $(egrep -v '^#' $HOME/.env | xargs)
fi

#
# logging on stdout
# Param #1: log level, e.g. INFO, WARN, ERROR
# Param #2: log message
log_echo () {
    LOG_LEVEL=$1
    LOG_MSG=$2
    TS=$(date '+%Y-%m-%d %H:%M:%S,%s')
    echo "$TS - $SCRIPT_NAME - $LOG_LEVEL - $LOG_MSG" >&2
}

#
# check docker
# we expect the script to execute within the docker container
check_docker() {
	# Src: https://stackoverflow.com/a/20012536
	grep -Eq '/(lxc|docker)/[[:xdigit:]]{64}' /proc/1/cgroup

	if [ "$?" -ne "0" ]; then
		echo "Please run this script in docker container" >&2
		exit 1
	fi

}
