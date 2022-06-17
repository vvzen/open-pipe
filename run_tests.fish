#!/usr/local/bin/fish

# Clean up paths
#set --export --global PYTHONPATH ""
#set --export --global OPENPIPE_CONFIG_PATH ""

set --erase --path --global PYTHONPATH
set --erase --path --global OPENPIPE_CONFIG_PATH

echo "Appending openpipe to PYTHONPATH"
source ./openpipe/source_me.fish

echo -e "\n"
echo "PYTHONPATH: $PYTHONPATH"
echo "OPENPIPE_CONFIG_PATH: $OPENPIPE_CONFIG_PATH"
echo -e "\n"
echo "Running Open Pipe Unit Test suite"

# Are we running on Github?
if test -n "$GITHUB_ACTION"
    poetry run pytest tests --cov=openpipe --cov-report=xml
# Or on Gitlab?
else if test -n "$CI"
    poetry run  pytest tests --cov=openpipe --cov-report=xml
# Or locally?
else
    # Uncomment for capturing stdout even on passed tests
    #pytest tests -rP --cov=openpipe --cov-report html

    pytest tests --cov=openpipe --cov-report html
    set current_os (uname)

    if string match "$current_os" "Darwin" 1> /dev/null
        open htmlcov/index.html
    else if string match "$current_os" "Linux"
        gio open htmlcov/index.html
    end
end
