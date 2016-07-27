from atlas.Command import NotUndoable, Command
from exceptions import Exceptions
from requester.Requester import req, rest_request
from util import eprint


class Create(Command):
    def __init__(self, role_name, description=''):
        self.role_name = role_name
        self.description = description

    def _do(self):
        errors = {
            'message': 'Could not create the role {}'.format(self.role_name),
            'reasons': {
                409: 'The role already exists'
            }
        }

        role = req.post('jira', 'role', json={'name': self.role_name, 'description': self.description}, errors=errors)
        print('The role {} has been created'.format(self.role_name))
        return role

    def _undo(self):
        Delete(self.role_name).do()


class Get(NotUndoable):
    def __init__(self, role_name):
        self.role_name = role_name

    def _do(self):
        roles = GetAll().do() or []
        match = None
        for role in roles:
            if role['name'] == self.role_name:
                match = role
                break
        return match


class GetAll(NotUndoable):
    """Return a map of the roles:
    Ex:
    {
        'Administrator': ...,
        'Users': ...
    }"""

    def _do(self):
        errors = {
            'message': 'Could not get roles',
            'reasons': {
                403: 'You must be an administrator'
            }
        }

        return req.get('jira', 'role', errors=errors)


class Delete(NotUndoable):
    def __init__(self, role_name):
        self.role_name = role_name

    def _do(self):
        role = Get(self.role_name).do()
        role_id = None if role is None else role['id']
        errors = {
            'message': 'Could not delete role',
            'reasons': {
                404: 'Given id does not exist',
                409: 'Project role is used in schemes and roleToSwap query parameter is not given'
            }
        }

        response = req.delete('jira', 'role/{}'.format(role_id), errors=errors)
        print('The role {} has been deleted'.format(self.role_name))
        return response
