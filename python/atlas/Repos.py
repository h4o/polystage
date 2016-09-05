from python.atlas.Command import NotUndoable, Command
from python.requester.Requester import Requester

from python.exceptions import Exceptions
from python.util import ProgressBar


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
                404: 'The repository does not exist'
            }
        }
        result = Requester.req.get('stash', 'projects/{}/repos/{}/commits'.format(self.project_key, self.repo),
                                   errors=errors)
        return result['values']


class GetCommitDiff(NotUndoable):
    def __init__(self, project_key, repo, commit_id):
        self.project_key = project_key
        self.repo = repo
        self.commit_id = commit_id

    def _do(self):
        url = 'projects/{}/repos/{}/commits/{}/diff'.format(self.project_key, self.repo, self.commit_id)
        commit = Requester.req.get('stash', url)

        return commit


class GetAllCommitDiffs(NotUndoable):
    cache = {}

    def __init__(self, project_key, repo, force=False):
        self.project_key = project_key
        self.repo = repo
        self.force = force

    def _do(self):
        key = (self.project_key, self.repo)
        cache = GetAllCommitDiffs.cache
        if key not in cache or self.force:
            commits = GetCommits(self.project_key, self.repo).do()
            pb = ProgressBar(len(commits))
            cache[key] = []
            for commit in commits:
                diff = GetCommitDiff(self.project_key, self.repo, commit['id']).do()
                diff['commit'] = commit
                cache[key].append(diff)
                pb.increment()
                pb.print()
        diffs = cache[key]
        return diffs
