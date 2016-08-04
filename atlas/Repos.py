from atlas.Command import NotUndoable, Command
from exceptions import Exceptions

from requester.Requester import Requester


class Create(Command):
    def __init__(self, project_key, name, scm_id='git', forkable=True):
        self.project_key = project_key
        self.name = name
        self.scm_id = scm_id
        self.forkable = forkable

    def _do(self):
        errors = {
            'message': 'Could not create the repository {}'.format(self.name),
            'reasons': {
                409: 'The repository already exists'
            }
        }
        json = {
            'name': self.name,
            'scmId': self.scm_id,
            'forkable': self.forkable
        }

        Requester.req.post('stash', 'projects/{}/repos'.format(self.project_key), json=json, errors=errors)
        print('The repository {} has been created'.format(self.name))

    def _undo(self):
        Delete(self.project_key, self.name).do()


class Delete(NotUndoable):
    def __init__(self, project_key, repo_name):
        self.project_key = project_key
        self.repo_name = repo_name

    def _do(self):
        message = 'Could not delete the repo {} from the project {}'.format(self.repo_name, self.project_key)
        reason = 'The repo does not exist'
        repo = Get(self.project_key, self.repo_name).do() or {}
        repo_slug = repo.get('slug')
        if not repo_slug:
            raise Exceptions.RequestException(message, reason, None)
        Requester.req.delete('stash', 'projects/{}/repos/{}'.format(self.project_key, repo_slug))
        print('The repository {} from the project {} has been deleted'.format(self.repo_name, self.project_key))


class Get(NotUndoable):
    def __init__(self, project_key, repo_name):
        self.project_key = project_key
        self.repo_name = repo_name

    def _do(self):
        repos = GetAll(self.project_key).do()
        match = None
        for repo in repos:
            if repo['name'].upper() == self.repo_name.upper():
                match = repo
                break
        return match


class GetAll(NotUndoable):
    def __init__(self, project_key):
        self.project_key = project_key

    def _do(self):
        return Requester.req.get('stash', 'projects/{}/repos'.format(self.project_key))['values']


class GetCommits(NotUndoable):
    def __init__(self, project_key, repo):
        self.project_key = project_key
        self.repo = repo

    def _do(self):
        errors = {
            'message': 'Could not get commits for repository {} from project {}'.format(self.repo, self.project_key),
            'reasons': {
                400: 'One of the supplied id',
                404: 'The repository does not exist'
            }
        }
        result = Requester.req.get('stash', 'projects/{}/repos/{}/commits'.format(self.project_key, self.repo),
                                   errors=errors)
        return result['values']
