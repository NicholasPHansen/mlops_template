# Base image
FROM python:{{ cookiecutter.python_version }}-slim AS base

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

FROM base AS trainer

WORKDIR /code
COPY src src/
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY LICENSE LICENSE
COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install . --no-deps --verbose

FROM trainer AS dev

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    git \
    tmux \
    vim \
    openssh-client \
    && apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements_dev.txt requirements_dev.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install -e .[dev]
