FROM node:23.3-alpine3.19 AS esbuild
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json frontend/esbuild.js ./
RUN npm ci

COPY ./frontend/app ./app
RUN node esbuild.js

FROM python:3.11 AS builder
ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without=dev --no-root

FROM python:3.11-slim-buster AS runtime
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./app ./app
COPY ./templates ./templates

RUN mkdir static
COPY --from=esbuild ./app/build ./static/react

EXPOSE 8001
CMD ["python", "-m", "app.main"]