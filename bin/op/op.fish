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
    echo "op takes care of going to a target location and setting the correct environment."
    echo -e "\nEXAMPLES:"
    echo -e "\$ op go /some/abs/path"
    echo -e "\$ op go ../some/relative/path"
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
    echo $destination_path | get-context

    # Set environment variables
    set --global --export --prepend --path OPENPIPE_CONFIG_PATH $destination_path

    # Finally.. go
    echo "Going to" $destination_path
    cd $destination_path
end

# No subcommands provided?
if test (count $argv) -eq 0
    echo -e "\nop: no arguments provided!\n"
    _help
    exit 1
end

# Parse subcommands
switch $argv[1]
    case go
        if test (count $argv) -eq 1
            echo "'go' requires a destination directory (where you do you wanna go?)"
            exit 1
        end
        _go $argv[2]
end
