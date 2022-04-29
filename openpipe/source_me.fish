# Source this file in order to get 'op' and 'open-pipe' available

set this_dir (realpath (dirname (status -f)))

# Set the PATH
set new_path (realpath "$this_dir/../bin")
set path_is_already_appended (echo $PATH | grep $new_path -c)

if test $path_is_already_appended -eq 1
    echo "PATH is already set, skipping"
else
    set --global --export --prepend --path PATH $new_path
end

# Set the PYTHONPATH
set new_python_path (realpath "$this_dir/..")
set pythopath_is_already_appended (echo $PYTHONPATH | grep $new_python_path -c)

if test $pythopath_is_already_appended -eq 1
    echo "PYTHONPATH is already set, skipping"
else
    set --global --export --prepend --path PYTHONPATH $new_python_path
end

# Set the config path
set new_config_path "$this_dir/configs"
set config_already_appended (echo $OPENPIPE_CONFIG_PATH | grep $new_config_path -c)

if test $config_already_appended -eq 1
    echo "OPENPIPE_CONFIG_PATH is already set, skipping"
else
    set --global --export --prepend --path OPENPIPE_CONFIG_PATH $new_config_path
end
