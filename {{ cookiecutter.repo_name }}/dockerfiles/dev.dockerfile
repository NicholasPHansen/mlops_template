# Base image
FROM python:{{ cookiecutter.python_version }}-slim AS base

RUN apt update \
    && apt install --no-install-recommends -y build-essential gcc  \
    && apt clean && rm -rf /var/lib/apt/lists/*


WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --verbose

FROM base AS dev


RUN apt update && \
    apt install --no-install-recommends -y \
    git \
    tmux \
    vim \
    && apt clean && rm -rf /var/lib/apt/lists/*

COPY src src/
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY LICENSE LICENSE
COPY requirements_dev.txt requirements_dev.txt

RUN pip install -e .[dev]
