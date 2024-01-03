FROM python:3.11.6-slim-bookworm

ENV LANG C.UTF-8
ENV VIRTUAL_ENV_DISABLE_PROMPT=1
ENV POETRY_VIRTUALENVS_CREATE=false


# Install poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy poetry.lock and pyproject.toml
COPY poetry.lock pyproject.toml /app/

# Install dependencies to system without creating virtual environment
RUN poetry install --no-interaction --no-ansi --no-root

# add all parent directory to the image
ADD . /app
