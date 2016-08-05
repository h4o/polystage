from python.atlas import Projects, Repos, PermScheme
from python.scripts.Runner import ReversibleRunner, NeverUndo
from python.scripts.Util import create_basic_roles, grant_bitbucket_perms, add_users_to_project

from python.schema.yaml_loader import load_file


def load_multi_repo_file(file_name):
    file = load_file(file_name, 'schema/multi_repo_template.yml')
    params = file['params']
    params['name'] = params.get('name', params['key'])
    params['readers'] = params.get('readers', [])
    params['type'] = params.get('type', 'software')
    params['scheme_name'] = params['key'] + '_projects'
    params['lead'] = params['supervisors'][0]
    params['developers'] = set([dev for repo in file['repos'] for dev in repo['developers']])

    return file


def load(file_name):
    data = load_multi_repo_file(file_name)
    params, repos = data['params'], data['repos']
    script = ReversibleRunner()

    create_basic_roles(script)

    _create_project(params, script)
    _add_users_to_project(params, script)
    _create_repos(params, repos, script)
    _create_permissions(params, script)

    return script


def _create_project(params, script):
    script.do(Projects.CreateJira(params['key'], params['name'], params['lead'], project_type=params['type']))
    script.do(Projects.CreateBitbucket(params['key'], params['name']))


def _add_users_to_project(params, script):
    with NeverUndo(script) as never_undo:
        add_users_to_project(params['key'], never_undo, readers=params['readers'], developers=params['developers'],
                             supervisors=params['supervisors'])


def _create_repos(params, repos, script):
    for repo in repos:
        script.do(Repos.Create(params['key'], repo['name']))


def _create_permissions(params, script):
    scheme_name = params['scheme_name']
    script.do(PermScheme.Create(scheme_name))
    script.do(PermScheme.AssignToProject(params['key'], scheme_name))

    with NeverUndo(script) as never_undo:
        jira_perms = {
            'BROWSE_PROJECTS': {
                'projectRole': ['supervisors', 'developers']}}
        never_undo.do(PermScheme.UpdatePermissions(scheme_name, jira_perms))
        grant_bitbucket_perms(params['key'], never_undo,
                              readers=params['readers'],
                              writers=params['developers'],
                              admins=params['supervisors'])
