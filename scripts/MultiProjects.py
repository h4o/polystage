from atlas import Projects, PermScheme, Applinks, Roles, Repos, BitbucketPerm
from atlas.BitbucketPerm import Permission
from schema.yaml_loader import load
from scripts import Runner
from scripts.Runner import ReversibleRunner, NeverUndo
from util.util import pp, eprint


def load_multi_project_file(file_name):
    file = load(file_name, 'schema/multi_project_template.yml')
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


def load_multi_project(file_name):
    data = load_multi_project_file(file_name)
    params = data['params']
    script = ReversibleRunner()

    Runner.create_roles(script)
    _create_permissions(params, script)

    for p in data['projects']:
        _create_project(p, params, script)

    return script


def _create_project(project, params, script):
    script.do(Projects.CreateJira(project['key'], project['name'], project['lead'], project_type=params['type']))
    script.do(Projects.CreateBitbucket(project['key'], project['name']))

    with NeverUndo(script) as never_undo:
        if params['applink']:
            never_undo.do(Applinks.Link(project['key'], project['key']))
        for supervisor in project['supervisors']:
            never_undo.do(Projects.AddWithRole(project['key'], supervisor, 'supervisors'))
            never_undo.do(BitbucketPerm.GrantPermission(project['key'], supervisor, Permission.ADMIN))
        for developer in project['developers']:
            never_undo.do(Projects.AddWithRole(project['key'], developer, 'developers'))
            never_undo.do(BitbucketPerm.GrantPermission(project['key'], developer, Permission.WRITE))
        for reader in project['readers']:
            never_undo.do(Projects.AddWithRole(project['key'], reader, 'readers'))
            never_undo.do(BitbucketPerm.GrantPermission(project['key'], reader, Permission.READ))

    for repo in params['repositories']:
        script.do(Repos.Create(project['key'], repo))

    script.do(PermScheme.AssignToProject(project['key'], params['scheme_name']))


def _create_permissions(params, script):
    script.do(PermScheme.Create(params['scheme_name']))

    with NeverUndo(script) as never_undo:
        scheme_name = params['scheme_name']
        never_undo.do(PermScheme.CreatePermission(scheme_name, 'projectRole', 'developers', 'BROWSE_PROJECTS'))
        never_undo.do(PermScheme.CreatePermission(scheme_name, 'projectRole', 'supervisors', 'BROWSE_PROJECTS'))
        never_undo.do(PermScheme.CreatePermission(scheme_name, 'projectRole', 'supervisors', 'ADMINISTER_PROJECTS'))
