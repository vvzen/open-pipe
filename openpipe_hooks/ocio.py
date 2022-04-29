import os
import shutil
import filecmp

import openpipe.log

log = openpipe.log.get_logger('openpipe_ocio')
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIGS_DIR = os.path.join(CURRENT_DIR, "..", "openpipe", "configs")


def setup_ocio_for_show(show_name, root_path):
    log.warning("No hook defined for 'hooks.ocio.setup_ocio_for_show'")
    log.info("Using default implementation.")

    source_config = os.path.join(CONFIGS_DIR, "aces_rec709_view.ocio")
    destination_dir = os.path.join(root_path, show_name, "openpipe", "etc")
    destination_path = os.path.join(destination_dir, "config.ocio")

    # NB: this is currently heavily coupled with the show schema tree
    if not os.path.exists(os.path.dirname(destination_dir)):
        log.error("The show is missing an expected directory: '%s'",
                  destination_dir)
        raise RuntimeError("Error during OCIO config copy. "
                           "See error message above^.")


    if os.path.exists(destination_path):
        log.info("\tDestination path exists already: %s", destination_path)
        are_same_file = [
            filecmp.cmp(source_config, destination_path),
            os.path.samefile(source_config, destination_path),
        ]
        if any(are_same_file):
            log.warning(("\tSkipping OCIO config copy "
                         "since file already exists."))
            return

    shutil.copyfile(source_config, destination_path)
    log.info("\tOCIO config copied to %s", destination_path)
