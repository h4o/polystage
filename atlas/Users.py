from atlas import Groups
from atlas.Command import NotUndoable, Command
from exceptions import Exceptions
from requester.Requester import req, rest_request
from util import eprint


class Create(Command):
    def __init__(self, user):
        self.user = user

    def _do(self):
        errors = {
            'message': 'Could not register {}'.format(self.user.fullname),
            'reasons': {
                400: 'Malformed request or the user already exists',
                403: 'The application is not allowed to create a new user'
            }
        }

        req.post('crowd', 'user', json=self.user.get_crowd_format(), errors=errors)
        print('The user {} has been registered'.format(self.user.display_name))

    def _undo(self):
        Remove(self.user).do()


class Remove(NotUndoable):
    def __init__(self, user):
        self.user = user

    def _do(self):
        errors = {
            'message': 'Could not delete user {}'.format(self.user.display_name),
            'reasons': {
                403: 'The application is not allowed to remove the user',
                404: 'The user could not be found'
            }
        }

        req.delete('crowd', 'user', params={'username': self.user.username}, errors=errors)
        print('The user {} as been deleted'.format(self.user.display_name))


class RemoveMany(NotUndoable):
    def __init__(self, users):
        self.users = users

    def _do(self):
        for user in self.users:
            Remove(user).do()


class RemoveFromGroup(NotUndoable):
    def __init__(self, user, group):
        self.group = group
        self.user = user

    def _do(self):
        errors = {
            'message': 'Could not remove the user {} from the group {}'.format(self.user, self.group),
            'reasons': {
                403: 'The application is not allowed to delete the membership',
                404: 'The user or group could not be found'
            }
        }
        json = {'username': self.user, 'groupname': self.group}
        req.delete('crowd', 'user/group/direct', json=json, errors=errors)
        print('The user {} has been removed from the group {}'.format(self.user, self.group))


class AddToGroup(Command):
    def __init__(self, username, group):
        self.username = username
        self.group = group

    def _do(self):
        errors = {
            'message': 'Could not add {} to group {}'.format(self.username, self.group),
            'reasons': {
                400: 'The group could not be found',
                403: 'The application is not allowed to add the membership',
                404: 'The user could not be found',
                409: 'The user is already a direct member of the group'
            }
        }
        params = {'username': self.username}
        json = {'name': self.group}

        req.post('crowd', 'user/group/direct', params=params, json=json, errors=errors)
        print('The user {} has been added to the group {}'.format(self.username, self.group))

    def _undo(self):
        RemoveFromGroup(self.username, self.group).do()
