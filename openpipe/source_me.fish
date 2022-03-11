# Source this file to append the library to your pythonpath
set new_python_path (realpath .)
set is_already_appended (echo $PYTHONPATH | grep $new_python_path -c)

if test $is_already_appended -eq 1
    echo "variable is already set, skipping"
    exit 1
end

set --global --export --prepend --path PYTHONPATH $new_python_path
