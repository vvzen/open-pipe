"""General utilities needed when dealing with shows (aka projects)
"""

import os
import enum
import shutil
import traceback

import openpipe.log
import openpipe.config
import openpipe.show_scheme.core
from openpipe.sanitization.core import name_for_filesystem

log = openpipe.log.get_logger("show")

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SHOW_SCHEME_DIR = os.path.join(CURRENT_DIR, "schema", "v001")

# -----------------------------------------------------------------------------
def create_show_on_disk(show_name, root_path):
    log.info("\tCreating show on disk..")

    show_path = os.path.join(root_path, show_name)
    if os.path.exists(show_path):
        log.warning("The top level dir '%s' already exists.", show_path)
        log.warning("The show might be already setup on disk. Skipping step..")
        return

    openpipe.show_scheme.core.create_project(show_name, root_path)


def setup_ocio_for_show(show_name, root_path):
    log.info("\tSetting up default OCIO config")

    source_config = os.path.join(CURRENT_DIR, "configs", "aces_rec709_view.ocio")
    destination_dir = os.path.join(root_path, show_name, "openpipe", "etc")
    destination_path = os.path.join(destination_dir, "config.ocio")

    # NB: this is currently heavily coupled with the show schema tree
    if not os.path.exists(os.path.dirname(destination_dir)):
        log.error("The show is missing an expected directory: '%s'",
                  destination_dir)
        raise RuntimeError("Error during OCIO config copy. "
                           "See error message above^.")

    shutil.copyfile(source_config, destination_path)
    log.info("\tOCIO config copied to %s", destination_path)


class ShowCreationSteps(enum.Enum):
    on_disk = create_show_on_disk
    setup_ocio = setup_ocio_for_show


DEFAULT_STEPS = [
    ShowCreationSteps.on_disk,
    ShowCreationSteps.setup_ocio
]


def get_show_root():
    openpipe_config = openpipe.config.get_config("openpipe")
    if "show" not in openpipe_config:
        raise openpipe.config.MalformedConfigError(
                "Missing 'show' key in 'openpipe.toml' config.")

    show_config = openpipe_config.get("show")
    root_mount_path = show_config.get("root_mount_path")

    if "root_mount_path" not in show_config or not root_mount_path:
        raise openpipe.config.MalformedConfigError(
                "Missing 'show.root_mount_path' key in 'openpipe.toml' config.")

    return root_mount_path


def create_show(name, steps=DEFAULT_STEPS):

    log.info("Show creation has started.")
    log.info("The request is to create a show with name '%s'", name)

    safe_project_name = name_for_filesystem(name)

    if safe_project_name != name:
        log.info("For safety reasons, the project name was automatically "
                 "converted from '%s' to '%s'", name, safe_project_name)
        reply = input("Is that ok? y/n:  ")
        if reply.lower() not in ["y", "yes"]:
            log.info("User did not agree with project name change. Exiting..")
            return

    show_root = get_show_root()
    log.info("show_root: %s", show_root)

    # Run the show creation steps
    for step in steps:
        step_name = step.__name__
        log.info("Executing step: %s", step_name)

        try:
            step(safe_project_name, show_root)
        except Exception:
            log.error("Failed to run step '%s'", step_name)
            log.error("Follows original exception:")
            traceback.print_exc()
            return

    log.info("Show creation completed.")
