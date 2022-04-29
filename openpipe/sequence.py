"""General utilities needed when dealing with shots (aka projects)
"""
import os
import traceback

import openpipe.show
import openpipe.log
import openpipe.config
from openpipe.naming import is_sequence

log = openpipe.log.get_logger('openpipe.sequence')

# -----------------------------------------------------------------------------
class SequenceCreationSteps(object):
    setup_on_disk = "setup_on_disk"
    setup_on_ftrack = "setup_on_ftrack"

ALL_STEPS = [
    SequenceCreationSteps.setup_on_disk,
    SequenceCreationSteps.setup_on_ftrack,
]

DEFAULT_STEPS = [
    SequenceCreationSteps.setup_on_disk,
]

# -----------------------------------------------------------------------------
def create_sequence_on_disk(sequence_name):

    config = openpipe.config.get_config("show_naming")
    sequence_config = config.get("sequence")

    # First, validation
    if not is_sequence(sequence_name):
        regex_description = sequence_config.get('description')
        log.warning("A valid sequence name should be:\n\t%s", regex_description)
        raise ValueError("'%s' is not a valid sequence name. "
                         "See the above^ log for more info.")

    show_root = openpipe.show.get_show_root()
    show_name = openpipe.show.get_current_show_name()
    sequence_path = os.path.join(show_root, show_name, sequence_name)
    if not os.path.exists(sequence_path):
        log.info("Creating %s", sequence_path)
        os.makedirs(sequence_path)
    else:
        log.info("Sequence %s already exists on disk, skipping.",
                 sequence_name)

    return sequence_path

def create_sequence_on_ftrack(name):
    try:
        import openpipe_hooks.ftrack
        return openpipe_hooks.ftrack.create_sequence(name)
    except ImportError:
        log.warning("No hook defined for 'hooks.ftrack.create_sequence")
        log.warning("Skipping.")


STEP_FUNCTION_MAP = {
    SequenceCreationSteps.setup_on_disk: create_sequence_on_disk,
    SequenceCreationSteps.setup_on_ftrack: create_sequence_on_ftrack,
}


# -----------------------------------------------------------------------------
def create_sequence(name, steps=DEFAULT_STEPS, raise_exc=False):
    log.info("Sequence creation has started.")
    log.info("Sequence name is '%s'", name)

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