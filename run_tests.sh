#!/bin/bash

# Clean up paths
export PYTHONPATH=""
export OPENPIPE_CONFIG_PATH=""

echo "Appending openpipe to PYTHONPATH"
source ./openpipe/source_me.bash
echo -e "\n"
echo "PYTHONPATH: $PYTHONPATH"
echo "OPENPIPE_CONFIG_PATH: $OPENPIPE_CONFIG_PATH"
echo -e "\n"
echo "Running Open Pipe Unit Test suite"

# Are we running on Github?
if [ -n $GITHUB_ACTION ]; then
    poetry run pytest tests --cov=openpipe --cov-report=xml
# Or on Gitlab?
elif [ -n $CI ]; then
    poetry run  pytest tests --cov=openpipe --cov-report=xml
# Or locally?
else
    pytest tests --cov=openpipe --cov-report term-missing
fi
