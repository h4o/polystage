from python.atlas import Roles
from python.atlas.Command import NotUndoable, Command

from python.requester import Requester


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
        Requester.req.post('jira', 'project/{}/role/{}'.format(self.project_key, role_id), json={'user': [self.user]},
                           errors=errors)
        print('The user {} has been added to the project {} for the role {}'.format(self.user, self.project_key,
                                                                                    self.role_name))


class CreateJira(Command):
    def __init__(self, key, name, lead, description='', project_type='business', category=''):
        self.key = key
        self.name = name
        self.lead = lead
        self.description = description
        self.project_type = project_type
        self.category = category

    def _do(self):
        """The key must be in uppercase, and its length in [2,10]
        """
        cate = GetCategory(self.category).do()
        cate_id = -1 if cate is None else cate['id']
        project = {
            'key': self.key,
            'name': self.name,
            'projectTypeKey': self.project_type,
            'description': self.description,
            'lead': self.lead,
        }
        if cate is not None:
            project['categoryId'] = cate_id
        errors = {
            'message': 'Could not create jira project {}'.format(self.key),
            'reasons': {
                400: 'Invalid request. Leader unknown or the project already exists'
            }
        }
        response = Requester.req.post('jira', 'project', json=project, errors=errors)
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
        response = Requester.req.post('stash', 'projects', json=project, errors=errors)
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
        Requester.req.delete('jira', 'project/{}'.format(self.key), errors=errors)
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
        Requester.req.delete('stash', 'projects/{}'.format(self.key), errors=errors)
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
        return Requester.req.get('jira', 'project/{}'.format(key), errors=errors)


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
        return Requester.req.get('stash', 'projects/{}'.format(key), errors=errors)


class GetAllJira(NotUndoable):
    def _do(self):
        return Requester.req.get('jira', 'project')


class GetIssues(NotUndoable):
    """Fetching every issues is long, so this command caches its result
    To force a new fetch, set the argument force to true"""

    cache = None

    def __init__(self, project_key, force=False):
        self.force = force
        self.project_key = project_key

    def _do(self):
        if GetIssues.cache is None or self.force:
            GetIssues.cache = Requester.req.get('jira', 'search?jql=project={}&maxResults=-1'.format(self.project_key))[
                'issues']
        return GetIssues.cache


class GetIssueTypes(NotUndoable):
    def _do(self):
        return Requester.req.get('jira', 'issuetype')


class GetFromTag(NotUndoable):
    def __init__(self, tag):
        self.tag = tag

    def _do(self):
        project_list = GetAllJira().do()
        projects = [a for a in project_list if 'projectCategory' in a and a['projectCategory']['name'] == self.tag]
        return projects


class CreateCategory(Command):
    def __init__(self, cate_name, description='unspecified'):
        self.cate_name = cate_name
        self.description = description

    def _do(self):
        errors = {
            'message': 'Could not create category {}'.format(self.cate_name),
            'reasons': {
                409: 'A category with the given name already exists'
            }
        }
        json = {
            'name': self.cate_name,
            'description': self.description
        }
        category = Requester.req.post('jira', 'projectCategory', json=json, errors=errors)
        print('The category {} has been created'.format(self.cate_name))
        return category

    def _undo(self):
        DeleteCategory(self.cate_name).do()


class GetCategory(NotUndoable):
    def __init__(self, cate_name):
        self.cate_name = cate_name

    def _do(self):
        categories = Requester.req.get('jira', 'projectCategory')
        category = [i for i in categories if i['name'] == self.cate_name]
        if not category:
            return None
        return category[0]


class DeleteCategory(NotUndoable):
    def __init__(self, cate_name):
        self.cate_name = cate_name

    def _do(self):
        cate = GetCategory(self.cate_name).do()
        errors = {
            'message': 'Could not delete the category {}'.format(self.cate_name),
            'reasons': {
                404: 'The category could not be found',
            }
        }
        cate_id = -1 if cate is None else cate['id']
        Requester.req.delete('jira', 'projectCategory/{}'.format(cate_id), errors=errors)
        print('The category {} has been deleted'.format(self.cate_name))
