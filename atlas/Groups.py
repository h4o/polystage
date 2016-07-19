from exceptions import Exceptions
from requester.Requester import req, rest_request
from util import eprint


@rest_request
def get_groups():
    errors = {
        'message': 'Could not get groups',
        'reasons': {
            400: 'Bad request'
        }
    }
    params = {'entity-type': 'group'}

    return req.get('crowd', 'search', params=params, errors=errors)['groups']


@rest_request
def create_jira(groups):
    for group in groups:
        errors = {
            'message': 'Could not create group {}'.format(group),
            'reasons': {
                400: 'Group already exists',
                403: 'Application is not allowed to create a new group'
            }
        }

        json = {'name': group, 'description': '', 'type': 'GROUP'}
        req.post('crowd', 'group', json=json, errors=errors)
        print('The group {} as been added'.format(group))


@rest_request
def delete_jira(group):
    errors = {
        'message': 'Could not delete group {}'.format(group),
        'reasons': {
            404: 'The group could not be found'
        }
    }

    req.delete('crowd', 'group', params={'groupname': group}, errors=errors)
    print('The group {} has been deleted'.format(group))
