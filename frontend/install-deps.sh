#!/bin/sh
# node_modules is a named volume, and `docker compose up --build` doesn't refresh it.
# Reinstall when the lockfile changes or node_modules lacks the required esbuild API.
set -e

STAMP=node_modules/.installed-package-lock.json

if ! cmp -s package-lock.json "$STAMP" ||
  ! node --input-type=module -e "import('esbuild').then(({ context }) => process.exit(typeof context === 'function' ? 0 : 1)).catch(() => process.exit(1))"; then
  echo "Frontend dependencies are stale or incompatible, reinstalling packages..."
  npm ci --no-audit --no-fund
  cp package-lock.json "$STAMP"
fi

exec "$@"
