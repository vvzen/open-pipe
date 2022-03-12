# Source this file to append the library to your pythonpath

new_python_path=$(realpath ..)
python_path_already_appended=$(echo $PYTHONPATH | grep $new_python_path -c)

if [ $python_path_already_appended == "1" ]; then
    echo "PYTHONPATH is already set correctly, skipping"
else
    export PYTHONPATH="$new_python_path:$PYTHONPATH"
fi

new_config_path=$(realpath ./openpipe/configs)
config_path_already_appended=$(echo $OPENPIPE_CONFIG_PATH| grep $config_path_already_appended -c)

if [ $config_path_already_appended == "1" ]; then
    echo "OPENPIPE_CONFIG_PATH is already set correctly, skipping"
else
    export OPENPIPE_CONFIG_PATH="$new_config_path:$OPENPIPE_CONFIG_PATH"
fi