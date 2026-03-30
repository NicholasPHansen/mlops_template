FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-alpine AS base

WORKDIR /code

COPY uv.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project

COPY src src/
COPY README.md README.md
COPY LICENSE LICENSE

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen

