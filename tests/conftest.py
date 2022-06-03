import os


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SAMPLES_DIR = os.path.join(CURRENT_DIR, "sample_files")


def add_openconfig_configs_to_pyfakefs(fs):
    """Add paths in the OPENPIPE_CONFIG_PATH as real directories in the
    pyfakefs virtual filesystem, so that can we access configs normally during
    our tests.
    """

    current_config_path = os.getenv("OPENPIPE_CONFIG_PATH")
    paths_to_search = current_config_path.split(":")

    for path in paths_to_search[::-1]:
        print(f"Adding {path} as real directory to pyfakefs")
        fs.add_real_directory(path)
