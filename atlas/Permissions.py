from atlas import Roles
from atlas.Command import NotUndoable
from exceptions import Exceptions
from requester.Requester import req, rest_request
from util import eprint


class Create(NotUndoable):
    def __init__(self, name):
        self.name = name

    def _do(self):
        errors = {
            'message': 'The permission scheme {} could not be created'.format(self.name),
            'reasons': {
                400: 'The scheme already exists or bad request'
            }
        }
        json = {
            'name': self.name
        }

        scheme = req.post('jira', 'permissionscheme', json=json, errors=errors)
        print('The permission scheme {} has been created'.format(self.name))
        return scheme


class Delete(NotUndoable):
    def __init__(self, name):
        self.name = name

    def _do(self):
        scheme = Get(self.name).do()
        req.delete('jira', 'permissionscheme/{}'.format(scheme['id']))
        print('The permission {} has been deleted'.format(self.name))


class CreatePermission(NotUndoable):
    def __init__(self, scheme_name, type, name, perm):
        self.scheme_name = scheme_name
        self.type = type
        self.name = name
        self.perm = perm

    def _do(self):
        """
        Type can be either group, projectRole or user
        """
        errors = {
            'message': 'Could not create the permission {} for the {} {}'.format(self.perm, type, self.name),
            'reasons': {
                400: 'Bad arguments'
            }
        }

        scheme = Get(self.scheme_name).do()
        json = {
            'holder': {
                'type': type,
                'parameter': GetEntityId(type, self.name).do()
            },
            'permission': self.perm.upper()
        }
        response = req.post('jira', 'permissionscheme/{}/permission'.format(scheme['id']), json=json,
                            params={'expand': 'group'}, errors=errors)
        print('The permission {} for the {} {} has been created'.format(self.perm, type, self.name))
        return response


class GetEntityId(NotUndoable):
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def _do(self):
        entity_id = None
        if type == 'group':
            entity_id = self.name
        elif type == 'projectRole':
            entity_id = Roles.Get(self.name).do().get('id', None)
            # entity_id = Roles.get(self.name).get('id', None)
        elif type == 'user':
            entity_id = self.name
        return entity_id


class Get(NotUndoable):
    def __init__(self, name):
        self.name = name

    def _do(self):
        schemes = GetAll().do() or []
        match = None
        for scheme in schemes:
            if scheme['name'].upper() == self.name.upper():
                match = scheme
                break
        if match is None:
            error = 'Could not get scheme {}'.format(self.name)
            reason = 'Scheme not found'
            e = Exceptions.RequestException(error, reason, None)
            raise e
        return match


class AssignToProject(NotUndoable):
    def __init__(self, project_key, scheme_name):
        self.project_key = project_key
        self.scheme_name = scheme_name

    def _do(self):
        scheme = Get(self.scheme_name).do()
        req.put('jira', 'project/{}/permissionscheme'.format(self.project_key), json={'id': scheme['id']})
        print('The scheme {} has been assigned to the project {}'.format(self.scheme_name, self.project_key))


class GetAll(NotUndoable):
    def _do(self):
        schemes = req.get('jira', 'permissionscheme')['permissionSchemes']
        return schemes
