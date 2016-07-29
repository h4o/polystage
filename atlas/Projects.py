from atlas import Roles
from atlas.Command import NotUndoable, Command
from requester.Requester import req, rest_request
from util.util import pp


class AddWithRole(NotUndoable):
    def __init__(self, project_key, user, role_name):
        self.project_key = project_key
        self.user = user
        self.role_name = role_name

    def _do(self):
        role = Roles.Get(self.role_name).do() or {}
        role_id = role.get('id', None)
        errors = {
            'message': 'Could not add user {} to the project {} for the role {}'.format(self.user, self.project_key,
                                                                                        self.role_name),
            'reasons': {
                404: 'Either the group, the role or the project does not exist or the user is already in it'
            }
        }
        req.post('jira', 'project/{}/role/{}'.format(self.project_key, role_id), json={'user': [self.user]},
                 errors=errors)
        print('The user {} has been added to the project {} for the role {}'.format(self.user, self.project_key,
                                                                                    self.role_name))


class CreateJira(Command):
    def __init__(self, key, name, lead, description='', project_type='business'):
        self.key = key
        self.name = name
        self.lead = lead
        self.description = description
        self.project_type = project_type

    def _do(self):
        """
        The key must be in uppercase, and its length in [2,10]
        """
        project = {
            'key': self.key,
            'name': self.name,
            'projectTypeKey': self.project_type,
            'description': self.description,
            'lead': self.lead
        }
        errors = {
            'message': 'Could not create jira project {}'.format(self.key),
            'reasons': {
                400: 'Invalid request. Leader unknown or the project already exists'
            }
        }
        response = req.post('jira', 'project', json=project, errors=errors)
        print('The jira project {} has been created'.format(self.key))
        return response

    def _undo(self):
        DeleteJira(self.key).do()


class CreateBitbucket(Command):
    def __init__(self, key, name, description=''):
        self.key = key
        self.name = name
        self.description = description

    def _do(self):
        project = {
            'key': self.key,
            'name': self.name,
            'description': self.description
        }
        errors = {
            'message': 'Could not create bitbucket project {}'.format(self.key),
            'reasons': {
                400: 'Validation error',
                409: 'The project key or name is already in use'
            }
        }
        response = req.post('stash', 'projects', json=project, errors=errors)
        print('The bitbucket project {} has been created'.format(self.key))
        return response

    def _undo(self):
        DeleteBitbucket(self.key).do()


class DeleteJira(NotUndoable):
    def __init__(self, key):
        self.key = key

    def _do(self):
        errors = {
            'message': 'Could not delete jira project {}'.format(self.key),
            'reasons': {
                403: 'You do not have the permissions to delete the project',
                404: 'The project does not exist'
            }
        }
        req.delete('jira', 'project/{}'.format(self.key), errors=errors)
        print('The jira project {} has been deleted'.format(self.key))


class DeleteBitbucket(NotUndoable):
    def __init__(self, key):
        self.key = key

    def _do(self):
        errors = {
            'message': 'Could not delete bitbucket project {}'.format(self.key),
            'reasons': {
                403: 'You do not have the permissions to delete the project',
                404: 'The project does not exist',
                409: 'The project can not be deleted as it contains repositories',
            }
        }
        req.delete('stash', 'projects/{}'.format(self.key), errors=errors)
        print('The bitbucket project {} has been deleted'.format(self.key))


class GetJira(NotUndoable):
    def __init__(self, key):
        self.key = key

    def _do(self):
        key = self.key.upper()
        errors = {
            'message': 'Could not get project {}'.format(key),
            'reasons': {
                404: 'Project not found'
            }
        }
        return req.get('jira', 'project/{}'.format(key), errors=errors)


class GetBitbucket(NotUndoable):
    def __init__(self, key):
        self.key = key

    def _do(self):
        key = self.key.upper()
        errors = {
            'message': 'Could not get project {}'.format(key),
            'reasons': {
                404: 'Project not found'
            }
        }
        return req.get('stash', 'projects/{}'.format(key), errors=errors)


class GetAllJira(NotUndoable):
    def _do(self):
        return req.get('jira', 'project')


class GetIssues(NotUndoable):
    """Fetching every issues is long, so this command caches its result
    To force a new fetch, set the argument force to true"""

    cache = None

    def __init__(self, project_key, force=False):
        self.force = force
        self.project_key = project_key

    def _do(self):
        if GetIssues.cache is None or self.force:
            GetIssues.cache = req.get('jira', 'search?jql=project={}&maxResults=-1'.format(self.project_key))['issues']
        return GetIssues.cache


class GetIssueTypes(NotUndoable):
    def _do(self):
        return req.get('jira', 'issuetype')


class GetFromTag(NotUndoable):
    def __init__(self, tag):
        self.tag = tag

    def _do(self):
        projects = GetAllJira().do()
        projects = [a for a in projects if a['key'].startswith(self.tag)]
        return projects
