from python.atlas import Projects, Repos, PermScheme
from python.scripts.Script import ReversibleRunner, NeverUndo, command
from python.scripts.Util import create_basic_roles, grant_bitbucket_perms, add_users_to_project, \
    grant_bitbucket_repo_perms

from python.schema.yaml_loader import load_file


@command
def load(file_name):
    data = load_multi_repo_file(file_name)
    params, repos = data['params'], data['repos']
    script = ReversibleRunner()

    _create_project(params, script)
    _create_repos(params, repos, script)
    _create_permissions(params, repos, script)

    return script


def load_multi_repo_file(file_name):
    file = load_file(file_name, 'python/schema/multi_repo_template.yml')
    params = file['params']
    params['name'] = params.get('name', params['key'])
    params['readers'] = params.get('readers', [])
    params['type'] = params.get('type', 'software')
    params['scheme_name'] = params['key'] + '_projects'
    params['lead'] = params['supervisors'][0]
    params['developers'] = set([dev for repo in file['repos'] for dev in repo['developers']])

    return file


def _create_project(params, script):
    script.do(Projects.CreateBitbucket(params['key'], params['name']))


def _create_repos(params, repos, script):
    for repo in repos:
        script.do(Repos.Create(params['key'], repo['name']))


def _create_permissions(params, repos, script):
    with NeverUndo(script) as never_undo:
        grant_bitbucket_perms(params['key'], never_undo,
                              readers=params['readers'],
                              admins=params['supervisors'])

        for repo in repos:
            grant_bitbucket_repo_perms(params['key'], repo['name'], never_undo,
                                       writers=repo['developers'])
