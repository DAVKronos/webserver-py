# Kronos website
FastAPI backend (`app/`) and React frontend (`frontend/`), run with Docker.

# Getting started
1. Clone the repository.
2. Get `config.toml` from the WebCie and put it in the repository root (`config.example.toml` shows the format).
3. Start everything:
   ```sh
   docker compose up --build
   ```

The site runs at http://localhost:8000. Changes to the backend and frontend are picked up automatically; refresh the browser to see them.

When `frontend/package.json` changes (e.g. after a pull), run `docker compose down -v` first, so the frontend's packages get reinstalled.

# Debugging Python in VSCode
Start with `docker compose -f docker-compose.yml -f docker-compose.dev.yml up`. The backend waits until a debugger attaches, using this `.vscode/launch.json` configuration:
```json
{
  "name": "Debug Python",
  "type": "debugpy",
  "request": "attach",
  "connect": { "host": "localhost", "port": 5678 },
  "justMyCode": false,
  "pathMappings": [{ "localRoot": "${workspaceFolder}", "remoteRoot": "/app" }]
}
```

# Debugging React in VSCode
```json
{
  "name": "Debug React",
  "type": "chrome",
  "request": "launch",
  "url": "http://localhost:8000",
  "webRoot": "${workspaceFolder}/frontend",
  "sourceMapPathOverrides": {
    "http://localhost:8000/static/app/*": "${workspaceFolder}/frontend/app/*"
  }
}
```
