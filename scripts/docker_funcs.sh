#
# Some functions to spin up docker containers
# and manage them.
#
# Authors: cdeck3r
#

# 
# Using docker compose the container name follows a convention
# Name: <dir with compose file>_<service name>_<int>
#
function docker_container_name()
{
  PRJ_NAME=$(echo $(basename $DOCKER_COMPOSE_DIR ) | tr '[:upper:]' '[:lower:]')
  echo ${PRJ_NAME}_${IMG_NAME}_1
}

# Determines the platform where the script runs
function platform()
{
    unameOut="$(uname -s)"
    case "${unameOut}" in
        Linux*)     machine=Linux;;
        Darwin*)    machine=Mac;;
        CYGWIN*)    machine=Cygwin;;
        MINGW*)     machine=MinGw;;
        *)          machine="UNKNOWN:${unameOut}"
    esac
    echo ${machine}
}

# returns running state of a given container 
function docker_runs()
{
    echo $(docker${docker_ext} inspect -f '{{.State.Running}}' $(docker_container_name))
}

#
# Check and spin up container
function docker_startup()
{
    CONTAINER_NAME=$(docker_container_name)
    
    if [ "$(docker_runs $CONTAINER_NAME)" != "true" ]; then
        log_echo "INFO" "Spin up container: $CONTAINER_NAME"
        cd $DOCKER_COMPOSE_DIR && docker-compose${docker_ext} up -d $IMG_NAME
        
        # re-check
        if [ "$(docker_runs $CONTAINER_NAME)" != "true" ]; then
            log_echo "ERROR" "Problem starting container: $CONTAINER_NAME"
            exit 1
        fi
    else
        log_echo "INFO" "Container runs: $CONTAINER_NAME"
    fi
}

# run a command using docker exec
function run_in_docker()
{
    local _EXEC_CMD=$1

    # some odd effect under windows output tty
    # See: https://superuser.com/a/1350903
    if [ "$(platform)" == "MinGw" ] || [ "$(platform)" == "Cygwin" ]; then
        docker_ext=.exe
    else 
        docker_ext=""
    fi

    # prepare ludwig's docker container
    docker_startup 
    # run ludwig command in container
    docker exec -it $(docker_container_name) /bin/bash -c "$_EXEC_CMD"
}

# shutdown: stop and remove container
function shutdown_container()
{
    # some odd effect under windows output tty
    # See: https://superuser.com/a/1350903
    if [ "$(platform)" == "MinGw" ] || [ "$(platform)" == "Cygwin" ]; then
        docker_ext=.exe
    else 
        docker_ext=""
    fi

    CONTAINER_NAME=$(docker_container_name)
    
    if [ "$(docker_runs)" == "true" ]; then
        log_echo "INFO" "Stop and remove container: $CONTAINER_NAME"
        docker${docker_ext} stop $CONTAINER_NAME
        docker${docker_ext} rm $CONTAINER_NAME
        
        # re-check
        if [ "$(docker_runs)" == "true" ]; then
            log_echo "ERROR" "Problem shutdown container: $CONTAINER_NAME"
            exit 1
        fi
        
    else
        log_echo "WARN" "Container does not run: $CONTAINER_NAME"
    fi

}
