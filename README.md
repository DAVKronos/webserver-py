

# Getting started (using Docker)
```sh
git clone git@github.com:DAVKronos/webserver-py.git
docker compose up --build
```

# Development environment
Launch with development settings:
```sh
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

# Debugging Python in VSCode
Modify `.vscode/launch.json` so that it contains:
```json
 {
            "name": "Debug Python",
            "type": "debugpy",
            "request": "attach",
            "connect": {
            "port": 5678,
            "host": "localhost",
            },
            "justMyCode": false,
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ]
        },
```
## Debugging React in VSCode
Modify `.vscode/launch.json` so that it contains:
```json
        {
            "type": "chrome",
            "request": "launch",
            "name": "Debug React",
            "url": "http://localhost:8001",
            "webRoot": "${workspaceFolder}/frontend/app"
          },
```
