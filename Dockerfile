FROM python:3.11
ENV POETRY_VERSION=1.6.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"
WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY app /app/app
COPY static /app/static
COPY templates /app/templates

EXPOSE 8000
CMD ["poetry","run", "python", "-m", "app.main"]