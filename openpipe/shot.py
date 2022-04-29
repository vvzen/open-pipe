"""General utilities needed when dealing with shots (aka projects)
"""
import os
import traceback

import openpipe.show
import openpipe.log
from openpipe.sequence import create_sequence, create_sequence_on_disk
from openpipe.config import MalformedConfigError
from openpipe.naming import (
    is_shot, sequence_name_from_shot_name
)

log = openpipe.log.get_logger('openpipe.shot')

# -----------------------------------------------------------------------------
class ShotCreationSteps(object):
    setup_on_disk = "setup_on_disk"
    setup_on_ftrack = "setup_on_ftrack"

ALL_STEPS = [
    ShotCreationSteps.setup_on_disk,
    ShotCreationSteps.setup_on_ftrack,
]

DEFAULT_STEPS = [
    ShotCreationSteps.setup_on_disk,
]

# -----------------------------------------------------------------------------

def create_shot_on_disk(shot_name):

    config = openpipe.config.get_config("show_naming")
    shot_config = config.get("shot")

    if not shot_config:
        raise MalformedConfigError("Naming entry for '%s' "
                                   "didn't contain a 'shot' key.")

    # First, validation
    if not is_shot(shot_name):
        regex_description = shot_config.get('description')
        log.warning("A valid shot name should be:\n\t%s", regex_description)
        raise ValueError("'%s' is not a valid shot name. "
                         "See the above^ log for more info." % shot_name)

    sequence_name = sequence_name_from_shot_name(shot_name)
    sequence_path = create_sequence_on_disk(sequence_name)

    shot_path = os.path.join(sequence_path, shot_name)
    if not os.path.exists(shot_path):
        log.info("Creating %s", shot_path)
        os.makedirs(shot_path)
    else:
        log.info("Shot %s already exists on disk, skipping.",
                 shot_name)

    return shot_path


def create_shot_on_ftrack(name):
    try:
        import openpipe_hooks.ftrack
        return openpipe_hooks.ftrack.create_shot(name)
    except ImportError:
        log.warning("No hook defined for 'hooks.ftrack.create_shot")
        log.warning("Skipping.")


STEP_FUNCTION_MAP = {
    ShotCreationSteps.setup_on_disk: create_shot_on_disk,
    ShotCreationSteps.setup_on_ftrack: create_shot_on_ftrack,
}


# ------------------------------------------------------------------------------
def create_shot(name, steps=DEFAULT_STEPS, raise_exc=False):
    log.info("Shot creation has started.")
    log.info("Shot name is '%s'", name)

    wrong_steps = [s for s in steps if s not in ALL_STEPS]
    if wrong_steps:
        log.error("These are not accepted steps: '%s'. Exiting..", wrong_steps)
        raise RuntimeError("Invalid steps provided. See log above^")

    # Run the show creation steps
    for step_name in steps:
        step_func = STEP_FUNCTION_MAP[step_name]
        log.info("Executing step: %s", step_name)

        try:
            step_func(name)
        except Exception:
            if raise_exc:
                raise
            else:
                log.error("Failed to run step '%s'", step_name)
                log.error("Follows original exception:")
                traceback.print_exc()
            return

    log.info("Shot creation completed.")
