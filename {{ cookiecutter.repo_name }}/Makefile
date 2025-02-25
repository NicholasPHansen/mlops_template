#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_VERSION = {{ cookiecutter.python_version }}
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 {{ cookiecutter.module_name }}
	isort --check --diff --profile black {{ cookiecutter.module_name }}
	black --check --config pyproject.toml {{ cookiecutter.module_name }}

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml {{ cookiecutter.module_name }}


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Make Dataset
.PHONY: data
data:
	$(PYTHON_INTERPRETER) src/{{ cookiecutter.module_name }}/dataset.py

## Train model
.PHONY: train
train:
	$(PYTHON_INTERPRETER) src/{{ cookiecutter.module_name }}/train.py

## Evaluate model
.PHONY: eval
eval:
	$(PYTHON_INTERPRETER) src/{{ cookiecutter.module_name }}/evaluate.py

## Visualize model
.PHONY: plots
plots:
	$(PYTHON_INTERPRETER) src/{{ cookiecutter.module_name }}/visualize.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)