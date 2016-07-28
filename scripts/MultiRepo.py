from atlas import Projects, Users, Repos, PermScheme, BitbucketPerm
from atlas.BitbucketPerm import Permission
from schema.yaml_loader import load
from scripts import Runner
from scripts.Runner import ReversibleRunner, NeverUndo
from util.util import pp


def load_multi_repo_file(file_name):
    file = load(file_name, 'schema/multi_repo_template.yml')
    params = file['params']
    params['name'] = params.get('name', params['key'])
    params['readers'] = params.get('readers', [])
    params['type'] = params.get('type', 'software')
    params['scheme_name'] = params['key'] + '_projects'
    params['lead'] = params['supervisors'][0]
    params['developers'] = set([dev for repo in file['repos'] for dev in repo['developers']])

    return file


def load_multi_repo(file_name):
    data = load_multi_repo_file(file_name)
    params, repos = data['params'], data['repos']
    script = ReversibleRunner()

    Runner.create_roles(script)

    _create_project(params, script)
    _add_dev_to_project(params, script)
    _create_repos(params, repos, script)
    _create_permissions(params, script)

    return script


def _create_project(params, script):
    script.do(Projects.CreateJira(params['key'], params['name'], params['lead'], project_type=params['type']))
    script.do(Projects.CreateBitbucket(params['key'], params['name']))


def _add_dev_to_project(params, script):
    for user in params['developers']:
        script.do(Projects.AddWithRole(params['key'], user, 'developers'), never_undo=True)


def _create_repos(params, repos, script):
    for repo in repos:
        script.do(Repos.Create(params['key'], repo['name']))


def _create_permissions(params, script):
    scheme_name = params['scheme_name']
    script.do(PermScheme.Create(scheme_name))
    script.do(PermScheme.AssignToProject(params['key'], scheme_name))

    with NeverUndo(script) as never_undo:
        never_undo.do(PermScheme.CreatePermission(scheme_name, 'projectRole', 'supervisors', 'BROWSE_PROJECTS'))
        never_undo.do(PermScheme.CreatePermission(scheme_name, 'projectRole', 'supervisors', 'ADMINISTER_PROJECTS'))

        for supervisor in params['supervisors']:
            never_undo.do(BitbucketPerm.GrantPermission(params['key'], supervisor, Permission.ADMIN))
        for developer in params['developers']:
            never_undo.do(BitbucketPerm.GrantPermission(params['key'], developer, Permission.WRITE))
