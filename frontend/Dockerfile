FROM node:23.3-alpine3.19

WORKDIR /app
COPY package.json package-lock.json esbuild.js ./
RUN npm ci

COPY ./app ./app
RUN node esbuild.js
CMD ["node", "esbuild.js", "--watch"]