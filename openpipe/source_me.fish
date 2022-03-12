# Source this file when you're doing dev stuff!

# Set the PYTHONPATH
set new_python_path (realpath .)
set pythopath_is_already_appended (echo $PYTHONPATH | grep $new_python_path -c)

if test $pythopath_is_already_appended -eq 1
    echo "PYTHONPATH is already set, skipping"
else
    set --global --export --prepend --path PYTHONPATH $new_python_path
end

# Set the config path
set new_config_path (realpath (dirname (status -f))/configs)
set config_already_appended (echo $OPENPIPE_CONFIG_PATH | grep $new_config_path -c)

if test $config_already_appended -eq 1
    echo "OPENPIPE_CONFIG_PATH is already set, skipping"
else
    set --global --export --prepend --path OPENPIPE_CONFIG_PATH $new_config_path
end
