#!/bin/sh
# node_modules is a named volume, and `docker compose up --build` doesn't refresh it.
# Reinstall whenever package-lock.json differs from the one node_modules was installed from.
set -e

STAMP=node_modules/.installed-package-lock.json

if ! cmp -s package-lock.json "$STAMP"; then
  echo "package-lock.json changed, reinstalling packages..."
  npm ci --no-audit --no-fund
  cp package-lock.json "$STAMP"
fi

exec "$@"
