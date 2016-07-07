from Requester import req
from exceptions import Exceptions
from util import eprint


def get_groups():
    errors = {
        'message': 'Could not get groups',
        'reasons': {
            400: 'Bad request'
        }
    }
    params = {'entity-type': 'group'}
    try:
        return req.get('crowd', 'search', params=params, errors=errors)['groups']
    except Exceptions.HTTPError as e:
        eprint(e)


def create(groups):
    for group in groups:
        errors = {
            'message': 'Could not create group {}'.format(group),
            'reasons': {
                400: 'Group already exists',
                403: 'Application is not allowed to create a new group'
            }
        }

        try:
            json = {'name': group, 'description': '', 'type': 'GROUP'}
            req.post('crowd', 'group', json=json, errors=errors)
            print('The group {} as been added'.format(group))
        except Exceptions.HTTPError as e:
            eprint(e)


def delete(groups):
    for group in groups:
        errors = {
            'message': 'Could not delete group {}'.format(group),
            'reasons': {
                404: 'The group could not be found'
            }
        }
        try:
            req.delete('crowd', 'group', params={'groupname': group}, errors=errors)
            print('The group {} has been deleted'.format(group))
        except Exceptions.HTTPError as e:
            eprint(e)
