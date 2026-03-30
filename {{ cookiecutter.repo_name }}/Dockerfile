FROM python:3.11-slim AS base

# Add uv
COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/

RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  make \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project

COPY src src/

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen
