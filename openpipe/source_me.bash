# Source this file to append the components of this library to the relevant paths

this_dir=$(realpath $(dirname $0))
new_python_path="$this_dir"

if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$new_python_path"
else
    python_path_already_appended=$(echo "$PYTHONPATH" | grep $new_python_path -c)
    if [[ $python_path_already_appended == "1" ]]; then
        echo "PYTHONPATH is already set correctly, skipping"
    else
        export PYTHONPATH="$new_python_path:$PYTHONPATH"
    fi
fi

new_config_path="$this_dir/openpipe/configs"

if [ -z "$OPENPIPE_CONFIG_PATH" ]; then
    export OPENPIPE_CONFIG_PATH="$new_config_path"
else
    config_path_already_appended=$(echo $OPENPIPE_CONFIG_PATH | grep $config_path_already_appended -c)
    if [[ $config_path_already_appended == "1" ]]; then
        echo "OPENPIPE_CONFIG_PATH is already set correctly, skipping"
    else
        export OPENPIPE_CONFIG_PATH="$new_config_path:$OPENPIPE_CONFIG_PATH"
    fi
fi