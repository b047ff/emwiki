#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../../emparser"

# Main
pipenv install
pipenv run python setup.py build
