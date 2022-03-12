import os

import yaml

import openpipe.log

log = openpipe.log.get_logger("config")


class MalformedConfigError(Exception):
    """Used to describe that a configuration doesn't have all the required keys.
    """

def get_config_path(name):

    current_config_path = os.getenv("OPENPIPE_CONFIG_PATH")
    if not current_config_path:
        raise EnvironmentError("OPENPIPE_CONFIG_PATH is not defined, "
                               "can't search.")

    matching_files = []
    paths_to_search = current_config_path.split(":")

    for path in paths_to_search[::-1]:
        if not os.path.exists(path):
            log.warning("Skipping non-existent path: %s", path)
            continue

        files = [
            os.path.join(path, f) for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f)) or
            os.path.islink(os.path.join(path, f))
        ]
        for file_path in files:
            base_name = os.path.basename(file_path)
            file_name, ext = os.path.splitext(base_name)
            if file_name == name:
                matching_files.append(file_path)

    log.debug("Found following configs: %s, using the top-most one.",
              matching_files)

    if not matching_files:
        raise OSError("No config files found with name: %s" % name)

    return matching_files[0]


def get_config(name):
    config_path = get_config_path(name)

    with open(config_path, "r") as f:
        config_data = f.read()

    config_parsed_data = yaml.safe_load(config_data)
    return config_parsed_data