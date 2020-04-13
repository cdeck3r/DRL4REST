# DRL4REST
Deep Reinforcement Learning for REST interfaces


## Quickstart

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


## Development IDE

Spin up vscode container

```bash
docker-compuse up -d vscode
```

Point your browser to it: https://127.0.0.1:8080

