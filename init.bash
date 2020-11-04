#!/bin/bash

# Setup dev environment, testing framework
# and code formatter
# copy pre commit hook
pip3 install -e .
pip3 install pytest
pip3 install black
cp pre-commit .git/hooks/pre-commit
