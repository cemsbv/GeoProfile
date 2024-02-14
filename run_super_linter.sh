#!/bin/bash

docker run \
--env VALIDATE_ALL_CODEBASE=false \
--env RUN_LOCAL=true \
--env VALIDATE_JSCPD=false \
--env VALIDATE_CSS=false \
--env VALIDATE_BASH=false \
--env VALIDATE_YAML=false \
--env VALIDATE_PYTHON_PYLINT=false \
--env VALIDATE_NATURAL_LANGUAGE=false \
--env VALIDATE_MARKDOWN=false \
--env LINTER_RULES_PATH=/ \
--env PYTHON_BLACK_CONFIG_FILE=pyproject.toml \
--env PYTHON_ISORT_CONFIG_FILE=pyproject.toml \
--env PYTHON_MYPY_CONFIG_FILE=pyproject.toml \
--env PYTHON_FLAKE8_CONFIG_FILE=.flake8 \
-v $(pwd):/tmp/lint github/super-linter:v4