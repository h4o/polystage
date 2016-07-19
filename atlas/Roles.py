from exceptions import Exceptions
from requester.Requester import req, rest_request
from util import eprint


@rest_request
def create(role_name, description=''):
    errors = {
        'message': 'Could not create the role {}'.format(role_name),
        'reasons': {
            409: 'The role already exists'
        }
    }

    role = req.post('jira', 'role', json={'name': role_name, 'description': description}, errors=errors)
    print('The role {} has been created'.format(role_name))
    return role


@rest_request
def get(role_name):
    roles = get_all() or []
    match = None
    for role in roles:
        if role['name'] == role_name:
            match = role
            break
    return match


@rest_request
def get_all():
    errors = {
        'message': 'Could not get roles',
        'reasons': {
            403: 'You must be an administrator'
        }
    }

    return req.get('jira', 'role', errors=errors)


@rest_request
def delete(role_name):
    role = get(role_name)
    role_id = None if role is None else role['id']
    errors = {
        'message': 'Could not delete role',
        'reasons': {
            404: 'Given id does not exist',
            409: 'Project role is used in schemes and roleToSwap query parameter is not given'
        }
    }

    response = req.delete('jira', 'role/{}'.format(role_id), errors=errors)
    print('The group has been deleted')
    return response
