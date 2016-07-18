from requester.Requester import req
from atlas import Roles
from exceptions import Exceptions
from util import eprint


def create(name):
    errors = {
        'message': 'The permission scheme {} could not be created'.format(name),
        'reasons': {
            400: 'The scheme already exists or bad request'
        }
    }
    json = {
        'name': name
    }
    try:
        scheme = req.post('jira', 'permissionscheme', json=json, errors=errors)
        print('The permission scheme {} has been created'.format(name))
        return scheme
    except Exceptions.RequestException as e:
        eprint(e)


def delete(name):
    try:
        scheme = get(name)
        req.delete('jira', 'permissionscheme/{}'.format(scheme['id']))
        print('The permission {} has been deleted'.format(name))
    except Exceptions.RequestException as e:
        eprint(e)


def create_permission(scheme_name, type, name, perm):
    """
    Type can be either group, projectRole or user
    """
    errors = {
        'message': 'Could not create the permission {} for the {} {}'.format(perm, type, name),
        'reasons': {
            400: 'Bad arguments'
        }
    }
    try:
        scheme = get(scheme_name)
        json = {
            'holder': {
                'type': type,
                'parameter': _get_entity_id(type, name)
            },
            'permission': perm.upper()
        }
        response = req.post('jira', 'permissionscheme/{}/permission'.format(scheme['id']), json=json,
                            params={'expand': 'group'}, errors=errors)
        print('The permission {} for the {} {} has been created'.format(perm, type, name))
        return response
    except Exceptions.RequestException as e:
        eprint(e)


def _get_entity_id(type, name):
    entity_id = None
    if type == 'group':
        entity_id = name
    elif type == 'projectRole':
        entity_id = Roles.get(name).get('id', None)
    elif type == 'user':
        entity_id = name
    return entity_id


def get(name):
    schemes = get_all() or []
    match = None
    for scheme in schemes:
        if scheme['name'].upper() == name.upper():
            match = scheme
            break
    if match is None:
        error = 'Could not get scheme {}'.format(name)
        reason = 'Scheme not found'
        e = Exceptions.RequestException(error, reason, None)
        raise e
    return match


def assign_to_project(project_key, scheme_name):
    try:
        scheme = get(scheme_name)
        req.put('jira', 'project/{}/permissionscheme'.format(project_key), json={'id': scheme['id']})
        print('The scheme {} has been assigned to the project {}'.format(scheme_name, project_key))
    except Exceptions.RequestException as e:
        eprint(e)


def get_all():
    try:
        schemes = req.get('jira', 'permissionscheme')['permissionSchemes']
        return schemes
    except Exceptions.RequestException as e:
        eprint(e)
