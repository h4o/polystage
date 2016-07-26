from atlas import Projects, Permissions, Applinks, Roles, Repos
from schema.yaml_loader import load
from scripts.Scripts import ReversibleRunner, NeverUndo
from util.util import pp


def load_multi_project_file(file_name):
    file = load(file_name, 'schema/new_project_template.yml')
    params = file['params']
    params['type'] = params.get('type', 'software')
    params['readers'] = params.get('readers', [])
    params['applink'] = params.get('applink', False)
    params['repositories'] = params.get('repositories', [])
    params['scheme_name'] = params['tag'] + '_projects'
    for project in file['projects']:
        project['key'] = params['tag'] + project['id']
        project['name'] = project.get('name', project['key'])
        project['lead'] = project.get('lead', project['developers'][0])
        project['supervisors'] = set(params['supervisors'] + project.get('supervisors', []))
        project['readers'] = set(params['readers'] + project.get('readers', []))
    return file


def load_multi_project(file_name, script=None):
    data = load_multi_project_file(file_name)
    params = data['params']
    if script is None:
        script = ReversibleRunner()

    _create_roles(script)

    for p in data['projects']:
        _create_project(p, params, script)

    _create_permissions(params['scheme_name'], script)

    return script


def _create_project(project, params, script):
    script.do(Projects.CreateJira(project['key'], project['name'], project['lead'], project_type=params['type']))
    script.do(Projects.CreateBitbucket(project['key'], project['name']))

    with NeverUndo(script) as never_undo:
        if params['applink']:
            never_undo.do(Applinks.Link(project['key'], project['key']))
        for developer in project['developers']:
            never_undo.do(Projects.AddWithRole(project['key'], developer, 'developers'))
        for supervisor in project['supervisors']:
            never_undo.do(Projects.AddWithRole(project['key'], supervisor, 'supervisors'))
        for reader in project['readers']:
            never_undo.do(Projects.AddWithRole(project['key'], reader, 'supervisors'))

    for repo in params['repositories']:
        script.do(Repos.Create(project['key'], repo))

    script.do(Permissions.AssignToProject(project['key'], params['scheme_name']))


def _create_roles(script):
    roles = script.do(Roles.GetAll())
    'developers' in roles or script.do(Roles.Create('developers'))
    'supervisors' in roles or script.do(Roles.Create('supervisors'))
    'readers' in roles or script.do(Roles.Create('readers'))


def _create_permissions(scheme_name, script):
    Permissions.Get(scheme_name).do(safe=True) or script.do(Permissions.Create(scheme_name))

    with NeverUndo(script) as never_undo:
        never_undo.do(Permissions.CreatePermission(scheme_name, 'projectRole', 'developers', 'BROWSE_PROJECTS'))
        never_undo.do(Permissions.CreatePermission(scheme_name, 'projectRole', 'supervisors', 'BROWSE_PROJECTS'))
        never_undo.do(Permissions.CreatePermission(scheme_name, 'projectRole', 'supervisors', 'ADMINISTER_PROJECTS'))
