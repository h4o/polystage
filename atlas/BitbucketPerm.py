from atlas.Command import NotUndoable
from requester.Requester import Requester


class Permission:
    ADMIN = 'PROJECT_ADMIN'
    READ = 'PROJECT_READ'
    WRITE = 'PROJECT_WRITE'


class GrantPermission(NotUndoable):
    def __init__(self, project_key, user_name, permission):
        self.permission = permission
        self.user_name = user_name
        self.project_key = project_key

    def _do(self):
        errors = {
            'message': 'Could not grant permission {} to user {} for project {}'.format(self.permission, self.user_name,
                                                                                        self.project_key),
            'reasons': {
                400: 'The permission does not exist'.format(self.permission),
                403: "The action was disallowed as it would reduce the currently authenticated user's permission level",
                404: 'The specified project or user does not exist'
            }
        }
        params = {
            'name': self.user_name,
            'permission': self.permission
        }
        Requester.req.put('stash', 'projects/{}/permissions/users'.format(self.project_key), params=params,
                          errors=errors)
        print('The permission {} has been granted to user {} for project {}'.format(self.permission, self.user_name,
                                                                                    self.project_key))
