# Development only: runs the esbuild watcher. ./frontend is bind-mounted over /app,
# so the image just provides Node and the initial contents of the node_modules volume.
FROM node:24-alpine

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund && cp package-lock.json node_modules/.installed-package-lock.json

# Outside /app so the bind mount doesn't hide it.
COPY install-deps.sh /usr/local/bin/install-deps.sh
ENTRYPOINT ["sh", "/usr/local/bin/install-deps.sh"]
CMD ["node", "esbuild.js", "--watch"]
