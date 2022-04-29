import openpipe.log

log = openpipe.log.get_logger('openpipe_hooks')

def create_project(show_name, root_path):
    log.warning("No hook defined for 'hooks.ftrack.create_project")
    log.warning("Skipping.")

def create_sequence(name):
    log.warning("No hook defined for 'hooks.ftrack.create_sequence")
    log.warning("Skipping.")

def create_shot(name):
    log.warning("No hook defined for 'hooks.ftrack.create_shot")
    log.warning("Skipping.")