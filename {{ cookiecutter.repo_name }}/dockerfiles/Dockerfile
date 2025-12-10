# Base image
FROM python:{{ cookiecutter.python_version }}-slim AS base

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc git openssh-client && \
    apt clean && rm -rf /var/lib/apt/lists/*

FROM base AS trainer

WORKDIR /code
COPY src src/
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY LICENSE LICENSE

RUN --mount=type=cache,target=/root/.cache/pip pip install . 

FROM trainer AS dev

# Install the library in edit mode and install development tools
RUN --mount=type=cache,target=/root/.cache/pip pip install -e .[dev]
