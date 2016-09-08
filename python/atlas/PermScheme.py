from python.atlas import Roles
from python.atlas.Command import NotUndoable, Command
from python.requester.Requester import Requester

from python.exceptions import Exceptions


class Create(Command):
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

        scheme = Requester.req.post('jira', 'permissionscheme', json=json, errors=errors)
        print('The permission scheme {} has been created'.format(self.name))
        return scheme

    def _undo(self):
        Delete(self.name).do()


class Delete(NotUndoable):
    def __init__(self, scheme_name):
        self.scheme_name = scheme_name

    def _do(self):
        scheme = Get(self.scheme_name).do()
        Requester.req.delete('jira', 'permissionscheme/{}'.format(scheme['id']))
        print('The permission {} has been deleted'.format(self.scheme_name))


class GrantPermission(Command):
    def __init__(self, scheme_name, e_type, name, perm):
        self.scheme_name = scheme_name
        self.type = e_type
        self.name = name
        self.perm = perm
        self.perm_id = None

    def _do(self):
        """
        Type can be either group, projectRole or user
        """
        errors = {
            'message': 'Could not create the permission {} for the {} {}'.format(self.perm, self.type, self.name),
            'reasons': {
                400: 'Bad arguments'
            }
        }

        scheme = Get(self.scheme_name).do()
        json = {
            'holder': {
                'type': self.type,
                'parameter': GetEntityId(self.type, self.name).do()
            },
            'permission': self.perm.upper()
        }
        response = Requester.req.post('jira', 'permissionscheme/{}/permission'.format(scheme['id']), json=json,
                                      errors=errors)
        print('The permission {} for the {} {} has been created'.format(self.perm, self.type, self.name))
        self.perm_id = response['id']
        return response

    def _undo(self):
        DeletePermission(self.scheme_name, self.perm_id).do()


class DeletePermission(NotUndoable):
    def __init__(self, scheme_name, permission_id):
        self.scheme_name = scheme_name
        self.permission_id = permission_id

    def _do(self):
        scheme = Get(self.scheme_name).do()
        Requester.req.delete('jira', 'permissionscheme/{}/permission/{}'.format(scheme['id'], self.permission_id))

        print('The permission {} for the scheme {} has been deleted'.format(self.permission_id, self.scheme_name))


class UpdatePermissions(NotUndoable):
    def __init__(self, scheme_name, permissions, description=''):
        """Permissions parameter must be a dict.
        Ex:
        {
            'ADMINISTER_PROJECTS': {
                'projectRole': ['supervisors'],
                'group': ['jira-administrator']
            },
            'BROWSE_PROJECTS': {
                'projectRole': ['readers', 'developers', 'supervisors'],
                'user': ['hc202796']
            }
        }
        """
        self.scheme_name = scheme_name
        self.perms = permissions
        self.description = description

    def _do(self):
        scheme = Get(self.scheme_name).do()
        perms = self.perms
        permissions = [
            {
                'holder': {
                    'type': e_type,
                    'parameter': GetEntityId(e_type, entity).do()
                },
                'permission': perm
            } for perm in perms for e_type in perms[perm] for entity in perms[perm][e_type]]

        params = {
            'name': self.scheme_name,
            'permissions': permissions
        }
        if self.description != '':
            params['description'] = self.description
        Requester.req.put('jira', 'permissionscheme/{}'.format(scheme['id']), json=params)
        print('The permission scheme {} has been updated'.format(self.scheme_name))


class GetEntityId(NotUndoable):
    def __init__(self, e_type, name):
        self.type = e_type
        self.name = name

    def _do(self):
        entity_id = None
        if self.type == 'group':
            entity_id = self.name
        elif self.type == 'projectRole':
            entity_id = Roles.Get(self.name).do().get('id', None)
        elif self.type == 'user':
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


class AssignToProject(Command):
    def __init__(self, project_key, scheme_name):
        self.project_key = project_key
        self.scheme_name = scheme_name

    def _do(self):
        scheme = Get(self.scheme_name).do()
        Requester.req.put('jira', 'project/{}/permissionscheme'.format(self.project_key), json={'id': scheme['id']})
        print('The scheme {} has been assigned to the project {}'.format(self.scheme_name, self.project_key))

    def _undo(self):
        AssignToProject(self.project_key, 'Default Permission Scheme').do()


class GetAll(NotUndoable):
    def _do(self):
        schemes = Requester.req.get('jira', 'permissionscheme')['permissionSchemes']
        return schemes
