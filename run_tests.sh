#!/bin/bash

echo "Appending openpipe to PYTHONPATH"
source ./openpipe/source_me.bash
echo "$PYTHONPATH"
echo "$OPENPIPE_CONFIG_PATH"
echo "Running Open Pipe Unit Test suite"
if [ ! -z $DEBUG ]; then
    pytest openpipe/test --cov=openpipe --cov-report term-missing
else
    pytest openpipe/test --cov=openpipe --cov-report=xml
fi