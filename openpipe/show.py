"""General utilities needed when dealing with shows (aka projects)
"""

import os
import traceback

import openpipe.log
import openpipe.config
import openpipe.show_scheme.core
from openpipe.filesystem import print_tree
from openpipe.sanitization.core import name_for_filesystem

log = openpipe.log.get_logger('openpipe.show')

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SHOW_SCHEME_DIR = os.path.join(CURRENT_DIR, "schema", "v001")

# -----------------------------------------------------------------------------
class ShowCreationSteps(object):
    setup_on_disk = "setup_on_disk"
    setup_ocio = "setup_ocio"
    setup_on_ftrack = "setup_on_ftrack"

ALL_STEPS = [
    ShowCreationSteps.setup_on_disk,
    ShowCreationSteps.setup_ocio,
    ShowCreationSteps.setup_on_ftrack,
]

DEFAULT_STEPS = [
    ShowCreationSteps.setup_on_disk,
    ShowCreationSteps.setup_ocio
]

# -----------------------------------------------------------------------------
def create_show_on_disk(show_name, root_path):
    log.info("\tCreating show on disk..")

    show_path = os.path.join(root_path, show_name)
    if os.path.exists(show_path):
        log.warning("The top level dir '%s' already exists.", show_path)
        log.warning("The show might be already setup on disk..")

    openpipe.show_scheme.core.create_project(show_name, root_path)
    log.info("Result on disk (first 4 levels) :")
    print_tree(show_path, max_level=4)


def setup_ocio_for_show(show_name, root_path):
    log.info("\tSetting up default OCIO config")
    import openpipe_hooks.ocio
    return openpipe_hooks.ocio.setup_ocio_for_show(show_name, root_path)


def create_project_on_ftrack(show_name, root_path):
    import openpipe_hooks.ftrack
    return openpipe_hooks.ftrack.create_project(show_name, root_path)


STEP_FUNCTION_MAP = {
    ShowCreationSteps.setup_on_disk: create_show_on_disk,
    ShowCreationSteps.setup_ocio: setup_ocio_for_show,
    ShowCreationSteps.setup_on_ftrack: create_project_on_ftrack,
}
# -----------------------------------------------------------------------------


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

    # To allow for testing under $HOME directories
    root_mount_path = os.path.expanduser(os.path.expandvars(root_mount_path))

    return root_mount_path


def create_show(name, steps=DEFAULT_STEPS, raise_exc=False):

    log.info("Show creation has started.")
    log.info("Show name is '%s'", name)

    wrong_steps = [s for s in steps if s not in ALL_STEPS]
    if wrong_steps:
        log.error("These are not accepted steps: '%s'. Exiting..", wrong_steps)
        raise RuntimeError("Invalid steps provided. See log above^")

    safe_project_name = name_for_filesystem(name)

    if safe_project_name != name:
        log.info("For safety reasons, the project name was automatically "
                 "converted from '%s' to '%s'", name, safe_project_name)
        reply = input("Is that ok? y/n:  ")
        if reply.lower() not in ["y", "yes"]:
            log.info("User did not agree with project name change. Exiting..")
            return

    show_root = get_show_root()
    log.info("Show root: %s", show_root)

    # To allow for testing under $HOME directories
    show_root = os.path.expanduser(os.path.expandvars(show_root))

    # Run the show creation steps
    for step_name in steps:
        step_func = STEP_FUNCTION_MAP[step_name]
        log.info("Executing step: %s", step_name)

        try:
            step_func(safe_project_name, show_root)
        except Exception:
            if raise_exc:
                raise
            log.error("Failed to run step '%s'", step_name)
            log.error("Follows original exception:")
            traceback.print_exc()
            return

    log.info("Show creation completed.")


def get_current_show_name():
    return os.environ["OPENPIPE_SHOW"]
