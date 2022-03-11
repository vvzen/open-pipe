# Source this file to append the library to your pythonpath
new_python_path=$(realpath .)
result=$(echo $PYTHONPATH | grep $new_python_path -c)

if [ $result == "1" ]; then
    echo "Path is already set correctly, skipping"
    exit 1
fi

export PYTHONPATH="$new_python_path:$PYTHONPATH"