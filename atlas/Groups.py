from atlas.Command import NotUndoable
from exceptions import Exceptions
from requester.Requester import req, rest_request
from util import eprint


class GetGroups(NotUndoable):
    def _do(self):
        errors = {
            'message': 'Could not get groups',
            'reasons': {
                400: 'Bad request'
            }
        }
        params = {'entity-type': 'group'}

        return req.get('crowd', 'search', params=params, errors=errors)['groups']


class CreateJira(NotUndoable):
    def __init__(self, groups):
        self.groups = groups

    def _do(self):
        for group in self.groups:
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


class DeleteJira(NotUndoable):
    def __init__(self, group):
        self.group = group

    def _do(self):
        errors = {
            'message': 'Could not delete group {}'.format(self.group),
            'reasons': {
                404: 'The group could not be found'
            }
        }

        req.delete('crowd', 'group', params={'groupname': self.group}, errors=errors)
        print('The group {} has been deleted'.format(self.group))
