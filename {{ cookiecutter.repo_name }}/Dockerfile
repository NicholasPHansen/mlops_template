FROM ubuntu:jammy

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt update && \
    apt install --no-install-recommends -y build-essential gcc git openssh-client curl ca-certificates && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /code

# Copy dependency manifests first for layer caching
COPY pyproject.toml pyproject.toml
COPY .python-version .python-version
COPY README.md README.md
COPY LICENSE LICENSE

# Install dependencies (cached until pyproject.toml changes)
RUN --mount=type=cache,target=/root/.cache/uv uv sync --no-install-project

# Copy source code and install project
COPY src src/
RUN --mount=type=cache,target=/root/.cache/uv uv sync
