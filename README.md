# DRL4REST
Deep Reinforcement Learning for REST interfaces

## Preps

Create a `.env` file in the project's root specifying global environment variables.
```
# In the container, this is the directory where the code is found
APP_ROOT=/DRL4REST

# the HOST directory containing directories to be mounted into containers
# e.g. /home/username/DRL4REST
VOL_DIR=<project root>
```

## Quickstart

Start in project's root dir. Create docker image
```bash
docker-compose build apigenerator 
```

Start in project's root dir. Generate API code:  
```bash
cd scripts
openapi-generator.sh
```
It generates python (client) and python-flask (server) code and places in the `openapi` directory. The default API is [thenounproject.com](https://raw.githubusercontent.com/APIs-guru/openapi-directory/master/APIs/thenounproject.com/1.0.0/swagger.yaml). 

Change the behavior with:
```
Usage : ./openapi-generator.sh [-h] [-a] [-n]

-a API_SPEC_URL
-n API_NAME 
```

Start the python client and server. Create docker image
and spin up the `pyclient` and `pyserver` container  
```bash
docker-compose up -d pyclient pyserver
```

Setup and start the server 
```bash
docker exec -it pyserver /bin/bash

cd /DRL4REST/scripts
./pyserver_setup.sh
```
Check the server is running pointing your browser to http://localhost:8000/ui/

In an other terminal setup the client
```bash
docker exec -it pyclient /bin/bash

cd /DRL4REST/scripts
./pyclient_setup.sh
```
Confirm that you can successfully download the API spec from the `pyserver` container from within the `pyclient` container.
```bash
 wget http://pyserver:8080/openapi.json
 ```

## Genetic Programming

Generally, we do not know the service behavior behind a REST interface, if there is only the interfac specification available. As a consequence, we plug-in a simulation, which is essentially a piece of code generating valid responses to concrete requests. 

Genetic Programming (GP) creates the program behind the REST interface. When a client sends a request to the REST interface, the created program generates an reply sent back to client. For GP we use the python [DEAP](https://github.com/deap/deap) framework. It is installed in a jupyter-scipy docker stack image.

Spin up the jupyscipy container
```bash
docker-compose up -d jupyscipy
```

Point your browser to http://localhost:8008 and test an example GP by loading and running the [`gp_test.ipynb`](blob/master/notebooks/gp_test.ipynb). It will find a regression function from data. A [tree graph](notebooks/graph.png) represents the regression function found by GP.

The notebook [`gp_cartpole_server.ipynb`](blob/master/notebooks/gp_cartpole_server.ipynb) shows the GP approach applied to the [cartpole](https://en.wikipedia.org/wiki/Inverted_pendulum) example. 


## Development IDE

Add a `.gitconfig` file  in the project's root with the following content.

```
[user]
	name = <git user name>
	email = <mail address>
[credential]
	helper = cache
```

Spin up vscode container

```bash
docker-compose up -d vscode
```

Point your browser to it: https://127.0.0.1:8080

The vscode docker image comes pre-installed with following extentions especially for working with shell scripts.

* [shfmt](https://github.com/mvdan/sh)
* [shellchecker](https://github.com/koalaman/shellcheck)

The shellchecker runs on-the-fly and provides quick fixes for better coding quality of shell scripts. The shfmt tool reformats the shell script. Use `shift + alt + f` to reformat the script.
