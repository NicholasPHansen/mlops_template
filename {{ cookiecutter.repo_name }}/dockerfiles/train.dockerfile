# Base image
FROM python:{{ cookiecutter.python_version }}-slim AS base

RUN apt update \
    && apt install --no-install-recommends -y build-essential gcc  \
    && apt clean && rm -rf /var/lib/apt/lists/*


WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --verbose

FROM base AS trainer

COPY src src/
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY LICENSE LICENSE

RUN pip install . --no-deps --no-cache-dir --verbose

ENTRYPOINT ["python", "-u", "src/{{ cookiecutter.project_name }}/train.py"]
