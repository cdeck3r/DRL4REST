# DRL4REST
Deep Reinforcement Learning for REST interfaces


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
It generates python (client) and python-flask (server) code and places in the `openapi` directory. The default API is [wmata.com/rail](https://raw.githubusercontent.com/APIs-guru/openapi-directory/master/APIs/wmata.com/rail-station/1.0/swagger.yaml). 

Change the behavior with:
```
Usage : ./openapi-generator.sh [-h] [-a] [-n]

-a API_SPEC_URL
-n API_NAME 
```

Start the python client and server. Create docker image
```bash
docker-compose build pyclient 
```

Spin up the `pyclient` and `pyserver` container  
```bash
docker-compose up -d pyclient pyserver
```

Install the client
```bash
docker exec -it pyclient /bin/bash

cd /DRL4REST/scripts
./pyclient_setup.sh
```

Install and start the server 
```bash
docker exec -it pyserver /bin/bash

cd /DRL4REST/scripts
./pyserver_setup.sh
```


## Development IDE

Spin up vscode container

```bash
docker-compose up -d vscode
```

Point your browser to it: https://127.0.0.1:8080

