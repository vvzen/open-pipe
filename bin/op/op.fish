# IMPORTANT: This script needs to be sourced, not executed

# NB: any CLI flag that we add via these options will be available as '_flag_something'
# For example: 'help' -> '_flag_help', etc.
set -l options (fish_opt --short h --long help)

# Additional args can be added like this:
#set options $options (fish_opt --short=m --long=max --required-val)

# Parse the cli args
argparse $options -- $argv

function _help
    echo -e "\nUSAGE"
    echo "op is a portable" (basename $SHELL) "script used to navigate the filesystem."
    echo "It takes care of going to a target location and setting the correct environment."
    echo -e "\nEXAMPLES\n"
    echo -e "Go to a shot/sequence"
    echo -e "\$ op go /some/abs/path"
    echo -e "\$ op go ../some/relative/path"
    echo -e "\n"
    echo -e "Show the current environment"
    echo -e "\$ op display-env"
    echo -e "\n"
    exit 1
end

if set -q _flag_help
   _help
end

# Implementation of filesystem navigation functionality
function _go
    set destination_path (realpath $argv)

    # Strip eventual '/' at the end
    set destination_splitted (string split '/' $destination_path)
    #set destination_length (string length $destination_splitted)[-1]
    if test (string length $destination_splitted)[-1] -eq 0
        set destination_path (string join '/' $destination_splitted[1..-2])
    end

    # Check destination is valid
    if not test -d $destination_path
        echo -e "Cannot 'go': $destination_path does not exist."
        return
    end

    # TODO: make into a single function since we use
    # this approach in different parts
    # Parse destination directory to understand environment
    set op_env_vars (string split \n -- (echo (realpath $destination_path) | get-context | tr "," "\n"))
    for openpipe_env_var in $op_env_vars
        set op_env_var_split (string split = $openpipe_env_var)
        set key $op_env_var_split[1]
        set value $op_env_var_split[2]
        if string match -v '*unknown*' $value > /dev/null
            if string match "DEBUG*" $OPENPIPE_LOG
                echo "Setting $key to $value"
            end
            set --global --export $key $value
        end
    end

    # Set environment variables

    # OPENPIPE_CONFIG_PATH
    # First: we search below
    set new_config_path "$destination_path/openpipe/etc/config"
    if test -d $new_config_path
        if not contains $new_config_path $OPENPIPE_CONFIG_PATH
            set --global --export --prepend --path OPENPIPE_CONFIG_PATH $new_config_path
        end
    end
    # Secondly, we search above
    # TODO:

    # OCIO
    set ocio_path "$destination_path/openpipe/etc/config.ocio"
    if test -e $ocio_path
        set --global --export --path OCIO $ocio_path
    end

    # PATH
    if string match 'bin' $destination_path
        set --global --export --prepend --path PATH $destination_path
    end
    # Custom env vars
    set custom_env_vars (command python -c 'import openpipe_hooks.env_vars as ev; ev.main()')
    for env_var in $custom_env_vars
        # TODO: protect against the use of '=' in environment vars values
        set env_var_split (string split = $env_var)
        set key $env_var_split[1]
        set value $env_var_split[2]
        if string match "DEBUG*" $OPENPIPE_LOG
            echo "Setting $key to $value"
        end
        set --global --export $key $value
    end

    # Finally.. go
    echo "Going to" $destination_path
    cd $destination_path
    set --global --export OPENPIPE_LAST_GO (realpath .)
end

function _display_env

    if ! test -n "$OPENPIPE_LAST_GO"
        echo "No OpenPipe environment detected."
        exit 1
    end

    echo -e "\nCurrent OpenPipe environment:\n"

    # Split by newline and build a list
    set env_vars (string split \n -- (echo $OPENPIPE_LAST_GO | get-context | tr "," "\n"))

    for env_var in $env_vars
        # Not sure why, but 'string match' seems to be printing to sdout
        if string match -v '*unknown*' $env_var > /dev/null
            echo "$env_var" | sed 's/=/: /g'
        end
    end

    echo "OPENPIPE_CONFIG_PATH:"
    for path in $OPENPIPE_CONFIG_PATH
        echo $path
    end

    printf "\n"
end

# No subcommands provided?
if test (count $argv) -eq 0
    echo -e "\nop: no arguments provided!\n"
    _help
    exit 1
end

# Parse subcommands
switch $argv[1]
    # op go some_dir
    case go
        if test (count $argv) -eq 1
            echo "'go' requires a destination directory (where you do you wanna go?)"
            exit 1
        end
        _go $argv[2]
    # op show
    case 'display-env'
        if test (count $argv) -ge 2
            echo "'display-env' currently accepts no arguments"
            exit 1
        end
        _display_env
end
