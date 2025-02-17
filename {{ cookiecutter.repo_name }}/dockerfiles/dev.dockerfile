# Base image
FROM python:{{ cookiecutter.python_version }}-slim AS base

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*


WORKDIR /
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --verbose

FROM base AS dev

COPY requirements_dev.txt requirements_dev.txt
RUN pip install -r requirements_dev.txt --no-cache-dir --verbose
RUN pip install -e .[dev]