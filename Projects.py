import Roles
from Requester import req
from exceptions import Exceptions
from schema import yaml_loader
from util import eprint


def import_projects(file_path):
    p = yaml_loader.load(file_path, 'schema/project_schema.yml')
    params = p['global']
    projects = p['projects']

    for project in projects:
        _import_project(project, params)


def _import_project(project, params):
    project_type = params.get('type', 'business')
    key = project.get('key') or project['name'][:10].replace(' ', '').upper()

    create(key, project['name'], project['lead'], project_type=project_type)

    dev_role = Roles.get('developers') or Roles.create('developers', 'The developers of the project')
    sup_role = Roles.get('supervisors') or Roles.create('supervisors', 'The supervisors of the project')

    for dev in project['developers']:
        add_with_role(key, dev, dev_role['id'])
    for sup in project.get('supervisors', []):
        add_with_role(key, sup, sup_role['id'])


def add_with_role(project_key, user, role_id):
    errors = {
        'message': 'Could not add user {} to the project {} for the role {}'.format(user, project_key, role_id),
        'reasons': {
            404: 'Either the group, the role or the project does not exist or the user is already in it'
        }
    }
    try:
        req.post('jira', 'project/{}/role/{}'.format(project_key, role_id), json={'user': [user]}, errors=errors)
        print('The user {} has been added to the project {} for the role {}'.format(user, project_key, role_id))
    except Exceptions.RequestException as e:
        eprint(e)


def create(key, name, lead, description='', project_type='business'):
    """
    The key must be in uppercase, and its length in [2:10]
    """
    project = {
        'key': key,
        'name': name,
        'projectTypeKey': project_type,
        'description': description,
        'lead': lead
    }
    errors = {
        'message': 'Could not create project {}'.format(name),
        'reasons': {
            400: 'Invalid request. Leader unknown or the project already exists'
        }
    }
    try:
        response = req.post('jira', 'project', json=project, errors=errors)
        print('The project {} has been created'.format(name))
        return response
    except Exceptions.RequestException as e:
        eprint(e)


def delete(key):
    errors = {
        'message': 'Could not delete project {}'.format(key),
        'reasons': {
            403: 'You do not have the permissions to delete the project',
            404: 'The project does not exist'
        }
    }
    try:
        req.delete('jira', 'project/{}'.format(key), errors=errors)
        print('The project {} has been deleted'.format(key))
    except Exceptions.RequestException as e:
        eprint(e)


def get(key):
    errors = {
        'message': 'Could not get project {}'.format(key),
        'reasons': {
            404: 'Project not found'
        }
    }
    try:
        return req.get('jira', 'project/{}'.format(key), errors=errors)
    except Exceptions.RequestException as e:
        eprint(e)


def get_all():
    try:
        return req.get('jira', 'project')
    except Exceptions.RequestException as e:
        eprint(e)
