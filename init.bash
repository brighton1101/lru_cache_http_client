#!/bin/bash

# Setup dev environment, testing framework
# and code formatter
# copy pre commit hook
python3 -m venv venv
source venv/bin/activate
pip3 install -e .
pip3 install pytest
pip3 install black
cp pre-commit .git/hooks/pre-commit
chmod u+x .git/hooks/pre-commit
