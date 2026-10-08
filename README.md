# Kronos website
FastAPI backend (`app/`) and React frontend (`frontend/`). Everything runs in Docker; you don't need Python or Node installed on your machine.

# Getting started
Requires Docker with Compose v2 (`docker compose`, not `docker-compose`).

```sh
git clone git@github.com:DAVKronos/webserver-py.git
cd webserver-py
cp config.example.toml config.toml   # then fill in the <...> values; ask the WebCie for the database credentials
docker compose up --build
```

The site is at http://localhost:8000. Two containers are started:

| Container | What it does |
|---|---|
| `kronos_python` | Runs the FastAPI backend on port 8000 and restarts it when a file in `app/` changes. |
| `kronos_frontend` | Runs esbuild in watch mode: every change in `frontend/app/` is rebuilt automatically. Refresh the browser to see it. |

> If you start the containers before creating `config.toml`, Docker creates an empty *directory* called `config.toml` and the backend fails to start. Remove that directory, copy the example file and start again.

# After pulling dependency changes
The frontend's `node_modules` lives in a Docker volume, and `--build` does **not** refresh it. When `frontend/package.json` or `frontend/package-lock.json` changed, recreate the volumes:
```sh
docker compose down -v
docker compose up --build
```
`-v` only removes the `frontend_node_modules` and `frontend_build` volumes; there is no database in this setup, so no data is lost.

Backend dependencies (`pyproject.toml` / `poetry.lock`) are installed into the image, so `docker compose up --build` is enough for those.

# Everyday commands
```sh
docker compose logs -f frontend                          # build output and errors from esbuild
docker compose run --rm frontend npm run lint            # ESLint
docker compose run --rm frontend npm install <package>   # add a frontend dependency (updates package.json and package-lock.json)
docker compose down                                      # stop everything
```

# Debugging Python in VSCode
Start the containers with the debug settings:
```sh
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```
The backend now **waits for a debugger before it starts**, so the site won't respond until you attach. Add this to `.vscode/launch.json` and run "Debug Python":
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Python",
      "type": "debugpy",
      "request": "attach",
      "connect": { "host": "localhost", "port": 5678 },
      "justMyCode": false,
      "pathMappings": [
        { "localRoot": "${workspaceFolder}", "remoteRoot": "/app" }
      ]
    }
  ]
}
```

# Debugging React in VSCode
The watch build includes source maps, so the browser's developer tools already show the original files (under `static/app/`). To set breakpoints from VSCode instead, add this configuration to `.vscode/launch.json` (next to the Python one) while the containers are running:
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

# Deployment
Pushing to `development` or `main` deploys automatically through GitHub Actions (`.github/workflows/deployment.yml`).
