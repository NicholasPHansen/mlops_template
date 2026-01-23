# Base image
FROM ubuntu:jammy AS base

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc git openssh-client curl ca-certificates && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

FROM base AS trainer

WORKDIR /code
COPY src src/
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY LICENSE LICENSE

# RUN --mount=type=cache,target=/root/.cache/pip pip install . 
RUN --mount=type=cache,target=/root/.cache/pip RUN uv sync --frozen

FROM trainer AS dev

# Install the library in edit mode and install development tools
RUN --mount=type=cache,target=/root/.cache/pip RUN uv sync --frozen --dev
