from Requester import req
from exceptions import Exceptions
from util import eprint


def create(role_name, description=''):
    errors = {
        'message': 'Could not create the role {}'.format(role_name),
        'reasons': {
            409: 'The role already exists'
        }
    }
    try:
        role = req.post('jira', 'role', json={'name': role_name, 'description': description}, errors=errors)
        print('The role {} has been created'.format(role_name))
        return role
    except Exceptions.RequestException as e:
        eprint(e)


def get(role_name):
    roles = get_all()
    if roles is None:
        return None
    match = None
    for role in roles:
        if role['name'] == role_name:
            match = role
            break
    return match


def get_all():
    errors = {
        'message': 'Could not get roles',
        'reasons': {
            403: 'You must be an administrator'
        }
    }
    try:
        return req.get('jira', 'role', errors=errors)
    except Exceptions.RequestException as e:
        eprint(e)