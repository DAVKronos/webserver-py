FROM node:24-alpine

WORKDIR /app
COPY package.json package-lock.json esbuild.js ./
RUN npm ci

COPY ./app ./app
RUN node esbuild.js
CMD ["node", "esbuild.js", "--watch"]