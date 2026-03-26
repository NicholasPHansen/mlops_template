# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a cookiecutter template for creating reproducible MLOps/Data Science projects. It's not a runnable project itself, but rather a generator that creates Python projects with a standardized structure, CI/CD pipelines, containerization, and development tools.

## Developing the Template

### Key Commands

**Generate a test project from the template:**
```bash
invoke template
```
This creates a new project directory with all template files rendered (cookiecutter variables replaced).

**Install template development dependencies:**
```bash
invoke requirements
```
Installs cookiecutter, pytest, pre-commit, and invoke from requirements.txt.

**Run tests and linting on the template itself:**
```bash
pytest
ruff check .
ruff format .
pre-commit run --all-files
```

**Validate pre-commit configuration:**
```bash
pre-commit validate-manifest
```

### Testing the Template

After making changes to the template, test by:
1. Running `invoke template` to generate a project
2. Navigating to the generated project directory
3. Installing dependencies: `pip install -r requirements.txt` (or use `uv sync` in generated projects)
4. Running the test commands in that project: `pytest`, `ruff check .`, etc.

## Template Structure

**Template files** are located in `{{ cookiecutter.repo_name }}/` and use Jinja2 templating:
- Variables like `{{ cookiecutter.project_name }}`, `{{ cookiecutter.author_name }}` are replaced when a project is generated
- Workflows in `.github/workflows/` are marked in `cookiecutter.json` with `_copy_without_render` to prevent template variable substitution

**Key template directories:**
- `{{ cookiecutter.repo_name }}/src/{{ cookiecutter.project_name }}/`: Core Python package with modular design
  - `data.py`: Data loading, cleaning, preprocessing
  - `model.py`: Model definitions
  - `train.py`: Training logic
  - `evaluate.py`: Model evaluation
  - `visualize.py`: Data and model visualization
  - `cli.py`: Typer-based CLI for project tasks
  - `config.py`: Configuration and directory paths
- `{{ cookiecutter.repo_name }}/tests/`: pytest test files
- `{{ cookiecutter.repo_name }}/dockerfiles/`: Multi-stage Dockerfile (base → trainer → dev)
- `{{ cookiecutter.repo_name }}/.devcontainer/`: VS Code devcontainer configuration

## Architecture

**Template Configuration** (`cookiecutter.json`):
- Defines prompts for: repo_name, project_name, author_name, description, python_version, license
- Specifies which files to skip Jinja2 rendering (GitHub workflows)

**Generated Project Stack:**
- **Package manager**: `uv` (modern, fast Python package manager)
- **Python dependencies**: torch, loguru, tqdm, typer, python-dotenv, torch-tb-profiler
- **Dev dependencies**: pytest, coverage, ruff, pre-commit, mkdocs, ipykernel
- **Linting & formatting**: ruff (configured in pyproject.toml)
- **Testing**: pytest with coverage reporting
- **CI/CD**: GitHub Actions workflows for tests (multi-OS, multi-Python version) and code linting
- **Containerization**: Docker with 2-stage builds
  - `base` stage: Ubuntu jammy + uv + build tools
  - `trainer` stage: Installs project dependencies
  - `dev` stage: Adds dev dependencies for interactive development
- **Development**: DevContainer with docker-compose, GPU support, VS Code extensions

**Docker Compose Services** (in generated projects):
- `dev`: Interactive development container with repo mounted, GPU support
- `trainer`: Isolated trainer container for reproducible model training

## Important Notes

When modifying the template:

1. **File paths with templating**: Use `{{ cookiecutter.variable }}` consistently across files
2. **Jinja2 filters**: The template uses `|tojson` in pyproject.toml to properly escape values like author_name
3. **Python version**: Defaults to 3.11 but should support 3.11+ (CI tests 3.11 and 3.12)
4. **CLI design**: Generated projects use Typer for CLI, not raw argparse or invoke
5. **Docker strategy**: Multi-stage builds share the base Ubuntu + uv layer to reduce image size
6. **pre-commit hooks**: Template includes hooks for trailing whitespace, docstrings, codespell, and pyproject validation
7. **Badge-ready**: README and workflows are ready for GitHub badges and status checks

## Common Modifications

**Adding a new dependency to all generated projects**:
- Edit `pyproject.toml` and add to `dependencies` or `[dependency-groups].dev`

**Adding a new CLI command to generated projects**:
- Add a function in `{{ cookiecutter.repo_name }}/src/{{ cookiecutter.project_name }}/cli.py` decorated with `@cli.command()`

**Updating CI/CD behavior**:
- Edit workflows in `{{ cookiecutter.repo_name }}/.github/workflows/`
- Update pytest, ruff, or coverage configuration in `pyproject.toml`

**Changing Docker base image or Python version**:
- Edit `{{ cookiecutter.repo_name }}/dockerfiles/Dockerfile`
- Update `.python-version` file (used by uv)
- Update `pyproject.toml` with `requires-python` constraint
