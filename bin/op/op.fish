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
    echo -e "\$ op show"
    echo -e "\n"
    exit 1
end

if set -q _flag_help
   _help
end

# Implementation of filesystem navigation functionality
function _go
    set destination_path $argv

    # Check destination is valid
    if not test -d $destination_path
        echo -e "Cannot 'go': $destination_path does not exist."
        return
    end

    # Parse destination directory to understand environment
    echo $destination_path | get-context > /dev/null

    # Set environment variables
    # Config
    if string match 'etc/config' $destination_path
        set --global --export --prepend --path OPENPIPE_CONFIG_PATH $destination_path
    end
    # Path
    if string match 'bin' $destination_path
        set --global --export --prepend --path PATH $destination_path
    end

    # Finally.. go
    echo "Going to" $destination_path
    cd $destination_path
end

function _show
    echo -e "\nCurrent OpenPipe environment:\n"

    # Split by newline and build a list
    set env_vars (string split \n -- (pwd | get-context | tr "," "\n"))

    for env_var in $env_vars
        # Not sure why, but 'string match' seems to be printing to sdout
        if string match -v '*unknown*' $env_var > /dev/null
            echo "$env_var" | sed 's/=/: /g'
        end
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
    case show
        if test (count $argv) -ge 2
            echo "'show' currently accepts no arguments"
            exit 1
        end
        _show
end
