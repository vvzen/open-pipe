#!/bin/bash

echo "Appending openpipe to PYTHONPATH"
source ./openpipe/source_me.bash
echo -e "\n"
echo "PYTHONPATH: $PYTHONPATH"
echo "OPENPIPE_CONFIG_PATH: $OPENPIPE_CONFIG_PATH"
echo -e "\n"
echo "Running Open Pipe Unit Test suite"
if [ ! -z $DEBUG ]; then
    pytest openpipe/test --cov=openpipe --cov-report term-missing
else
    pytest openpipe/test --cov=openpipe --cov-report=xml
fi