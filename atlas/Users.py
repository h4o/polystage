from atlas import Groups
from exceptions import Exceptions
from requester.Requester import req
from util import eprint


def create(user):
    errors = {
        'message': 'Could not register {}'.format(user.fullname),
        'reasons': {
            400: 'Malformed request or the user already exists',
            403: 'The application is not allowed to create a new user'
        }
    }
    try:
        req.post('crowd', 'user', json=user.get_crowd_format(), errors=errors)
        print('The user {} has been registered'.format(user.display_name))
    except Exceptions.RequestException as e:
        eprint(e)


def create_many(users):
    for user in users:
        create(user)


def remove(user):
    errors = {
        'message': 'Could not delete user {}'.format(user.display_name),
        'reasons': {
            403: 'The application is not allowed to remove the user',
            404: 'The user could not be found'
        }
    }
    try:
        req.delete('crowd', 'user', params={'username': user.username}, errors=errors)
        print('The user {} as been deleted'.format(user.display_name))
    except Exceptions.RequestException as e:
        eprint(e)


def remove_many(users):
    for user in users:
        remove(user)


def add_to_groups(user, groups, create=False):
    if create:
        Groups.create_jira(groups)
    for group in groups:
        errors = {
            'message': 'Could not add {} to group {}'.format(user.display_name, group),
            'reasons': {
                400: 'The group could not be found',
                403: 'The application is not allowed to add the membership',
                404: 'The user could not be found',
                409: 'The user is already a direct member of the group'
            }
        }
        params = {'username': user.username}
        json = {'name': group}
        try:
            req.post('crowd', 'user/group/direct', params=params, json=json, errors=errors)
            print('The user {} has been added to the group {}'.format(user.display_name, group))
        except Exceptions.RequestException as e:
            eprint(e)


def add_many_to_groups(users, groups, create=False):
    if create:
        Groups.create_jira(groups)
    for user in users:
        add_to_groups(user, groups)
