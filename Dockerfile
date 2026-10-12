FROM node:24-alpine AS esbuild
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json frontend/esbuild.js ./
RUN npm ci

COPY ./frontend/app ./app
RUN npm run build:prod

FROM python:3.11 AS builder
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.3

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without=dev --no-root

# Debian 10 (OpenSSL 1.1.1) on purpose: with Debian 12 (OpenSSL 3) the app couldn't reach the database
# on the server. Buster is end of life, so move on once the database side is sorted out.
FROM python:3.11-slim-buster AS runtime
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./app ./app
COPY ./templates ./templates

RUN mkdir static
COPY --from=esbuild /app/build ./frontend_build

EXPOSE 8000
CMD ["python", "-m", "app.main"]