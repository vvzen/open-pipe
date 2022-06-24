#!/bin/bash

source /net/pipeline/etc/bashrc

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
if [ -n "$GITHUB_ACTION" ]; then
    poetry run pytest tests --cov=openpipe --cov-report=xml
# Or on Gitlab?
elif [ -n "$CI" ]; then
    python3 -m pytest tests --cov=openpipe --cov-report=xml
# Or locally?
else
    # Uncomment for capturing stdout even on passed tests
    #pytest tests -rP --cov=openpipe --cov-report html

    pytest tests --cov=openpipe --cov-report html
    current_os=$(uname)
    if [ $current_os == "Darwin" ]; then
        open htmlcov/index.html
    elif [ $current_os == "Linux" ]; then
        gio open htmlcov/index.html
    fi
fi
