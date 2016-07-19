from atlas import Roles
from exceptions import Exceptions
from requester.Requester import req
from util import eprint


def add_with_role(project_key, user, role_name):
    role = Roles.get(role_name) or {}
    role_id = role.get('id', None)
    errors = {
        'message': 'Could not add user {} to the project {} for the role {}'.format(user, project_key, role_name),
        'reasons': {
            404: 'Either the group, the role or the project does not exist or the user is already in it'
        }
    }
    try:
        req.post('jira', 'project/{}/role/{}'.format(project_key, role_id), json={'user': [user]}, errors=errors)
        print('The user {} has been added to the project {} for the role {}'.format(user, project_key, role_name))
    except Exceptions.RequestException as e:
        eprint(e)


def create_jira(key, name, lead, description='', project_type='business'):
    """
    The key must be in uppercase, and its length in [2,10]
    """
    project = {
        'key': key,
        'name': name,
        'projectTypeKey': project_type,
        'description': description,
        'lead': lead
    }
    errors = {
        'message': 'Could not create jira project {}'.format(name),
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


def create_bitbucket(key, name, description=''):
    project = {
        'key': key,
        'name': name,
        'description': description
    }
    errors = {
        'message': 'Could not create bitbucket project {}'.format(name),
        'reasons': {
            400: 'Validation error',
            409: 'The project key or name is already in use'
        }
    }
    try:
        response = req.post('stash', 'projects', json=project, errors=errors)
        print('The bitbucket project {} has been created'.format(name))
        return response
    except Exceptions.RequestException as e:
        eprint(e)


def delete_jira(key):
    errors = {
        'message': 'Could not delete jira project {}'.format(key),
        'reasons': {
            403: 'You do not have the permissions to delete the project',
            404: 'The project does not exist'
        }
    }
    try:
        req.delete('jira', 'project/{}'.format(key), errors=errors)
        print('The jira project {} has been deleted'.format(key))
    except Exceptions.RequestException as e:
        eprint(e)


def delete_bitbucket(key):
    errors = {
        'message': 'Could not delete bitbucket project {}'.format(key),
        'reasons': {
            403: 'You do not have the permissions to delete the project',
            404: 'The project does not exist',
            409: 'The project can not be deleted as it contains repositories',
        }
    }
    try:
        req.delete('stash', 'projects/{}'.format(key), errors=errors)
        print('The bitbucket project {} has been deleted'.format(key))
    except Exceptions.RequestException as e:
        eprint(e)


def get_jira(key):
    key = key.upper()
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


def get_bitbucket(key):
    key = key.upper()
    errors = {
        'message': 'Could not get project {}'.format(key),
        'reasons': {
            404: 'Project not found'
        }
    }
    try:
        return req.get('stash', 'projects/{}'.format(key), errors=errors)
    except Exceptions.RequestException as e:
        eprint(e)


def get_all_jira():
    try:
        return req.get('jira', 'project')
    except Exceptions.RequestException as e:
        eprint(e)
