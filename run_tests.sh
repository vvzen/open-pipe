#!/bin/bash

echo "Appending openpipe to PYTHONPATH"
source ./openpipe/source_me.bash
echo "Running Open Pipe Unit Test suite"
pytest openpipe/test