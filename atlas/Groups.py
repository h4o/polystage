from atlas.Command import NotUndoable, Command

from requester.Requester import Requester


class GetAll(NotUndoable):
    def _do(self):
        errors = {
            'message': 'Could not get groups',
            'reasons': {
                400: 'Bad request'
            }
        }
        params = {'entity-type': 'group'}

        return Requester.req.get('crowd', 'search', params=params, errors=errors)['groups']


class Get(NotUndoable):
    def __init__(self, groupname):
        self.groupname = groupname

    def _do(self, safe=False):
        errors = {
            'message': 'Could not get the group {}'.format(self.groupname),
            'reasons': {
                404: 'The group was not found'
            }
        }
        return Requester.req.get('crowd', 'group', params={'groupname': self.groupname}, errors=errors)


class Create(Command):
    def __init__(self, group):
        self.group = group

    def _do(self):
        errors = {
            'message': 'Could not create group {}'.format(self.group),
            'reasons': {
                400: 'Group already exists',
                403: 'Application is not allowed to create a new group'
            }
        }

        json = {'name': self.group, 'description': '', 'type': 'GROUP'}
        Requester.req.post('crowd', 'group', json=json, errors=errors)
        print('The group {} as been created'.format(self.group))

    def _undo(self):
        Delete(self.group).do()


class Delete(NotUndoable):
    def __init__(self, group):
        self.group = group

    def _do(self):
        errors = {
            'message': 'Could not delete group {}'.format(self.group),
            'reasons': {
                404: 'The group could not be found'
            }
        }

        Requester.req.delete('crowd', 'group', params={'groupname': self.group}, errors=errors)
        print('The group {} has been deleted'.format(self.group))
