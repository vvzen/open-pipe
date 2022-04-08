import os

import ftrack_api
import ftrack_api.structure.id
import openpipe.log
from openpipe.show import get_show_root

log = openpipe.log.get_logger('ftrack-hook')


class FTrackEnvVars(object):
    # See https://ftrack-python-api.rtd.ftrack.com/en/2.3/environment_variables.html
    API_KEY = 'FTRACK_API_KEY'
    USER = 'FTRACK_API_USER'
    SERVER_URL = 'FTRACK_SERVER'
    EVENT_PLUGIN_PATH = 'FTRACK_EVENT_PLUGIN_PATH'
    API_SCHEMA_CACHE_PATH = 'FTRACK_API_SCHEMA_CACHE_PATH'

    REQUIRED_VARS = [API_KEY, USER, SERVER_URL]

    @classmethod
    def sanity_check_vars(cls):
        for env_var in cls.REQUIRED_VARS:
            if env_var not in os.environ:
                raise OSError(("Missing Required FTrack "
                               "environment var: %s" % env_var))


def new_session():

    FTrackEnvVars.sanity_check_vars()

    _api_key = os.environ[FTrackEnvVars.API_KEY]
    _studio_url = os.environ[FTrackEnvVars.SERVER_URL]
    _user = os.environ[FTrackEnvVars.USER]

    session = ftrack_api.Session(server_url=_studio_url,
                                 api_key=_api_key,
                                 api_user=_user,
                                 auto_connect_event_hub=True)

    return session


def create_project(show_name, root_path):

    session = new_session()

    # Check if a project with that name already exists on disk
    search_query = f'select name from Project where name is {show_name}'
    project = session.query(search_query).first()

    if project:
        log.error("Project with 'name=%s' already exists in ftrack. "
                  "Skipping creation..", show_name)
        return project

    user_query = f'User where email is "{session.api_user}"'
    current_user = session.query(user_query).one()
    assert current_user

    schema_name = 'VFX'
    schema_query = f'ProjectSchema where name is "{schema_name}"'
    vfx_schema = session.query(schema_query).one()
    assert vfx_schema

    # To check out the REST api schema, look at
    # https://yourstudio.ftrackapp.com/#Project
    full_name = ' '.join([w.capitalize() for w in show_name.split('_')])
    project_data = {
        'name': show_name,
        'full_name': full_name,
        'status': 'active',
        'created_by': current_user,
        'project_schema': vfx_schema,
        'root': root_path,
    }

    session.create('Project', project_data)

    log.info("Creating project %s in ftrack...", show_name)
    session.commit()

    project = session.query(search_query).one()

    # Create the first task of the project
    task_name = 'conforming'
    task_type = session.query('Type where name is "Editing"').one()
    task_status = session.query('Status where name is "Not started"').one()
    assert task_type
    assert task_status

    session.create('Task', {
        'name': task_name,
        'parent': project,
        'status': task_status,
        'type': task_type
    })

    log.info("Creating '%s' task", task_name)
    session.commit()

    # Send a desktop notification
    notification_message = (f'(TEST) Project "{show_name}" was just '
                            f'created by {current_user["first_name"]}.')
    message_data = {
        'type': 'message',
        'success': True,
        'message': notification_message
    }
    message_target = 'applicationId=ftrack.client.web'

    session.event_hub.publish(
        ftrack_api.event.base.Event(
            topic='show-creation',
            data=message_data,
            target=message_target
        ),
        synchronous=False,
    )

    log.info('All done.')

    return project