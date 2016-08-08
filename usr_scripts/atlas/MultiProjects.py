from python.atlas import Projects, PermScheme, Applinks, Repos
from python.scripts.Script import ReversibleRunner, NeverUndo, public
from python.scripts.Util import create_basic_roles, grant_bitbucket_perms, add_users_to_project

from python.schema.yaml_loader import load_file


@public
def load(file_name):
    data = load_multi_project_file(file_name)
    params = data['params']
    script = ReversibleRunner()

    create_basic_roles(script)
    _create_permissions(params, script)
    script.do(Projects.CreateCategory(params['tag']))

    for p in data['projects']:
        _create_project(p, params, script)

    return script


def load_multi_project_file(file_name):
    file = load_file(file_name, 'python/schema/multi_project_template.yml')
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


def _create_project(project, params, script):
    key, name, lead = project['key'], project['name'], project['lead']
    p_type, tag = project['type'], project['tag']
    readers, supervisors, developers = project['readers'], project['supervisors'], project['developers']

    script.do(Projects.CreateJira(key, name, lead, project_type=p_type, category=params['tag']))
    script.do(Projects.CreateBitbucket(key, name))

    with NeverUndo(script) as never_undo:
        if params['applink']:
            never_undo.do(Applinks.Link(key, key))
        add_users_to_project(key, never_undo, readers=readers, developers=developers, supervisors=supervisors)
        grant_bitbucket_perms(key, never_undo, readers=readers, writers=developers, admins=supervisors)

    for repo in params['repositories']:
        script.do(Repos.Create(key, repo))

    script.do(PermScheme.AssignToProject(key, params['scheme_name']))


def _create_permissions(params, script):
    script.do(PermScheme.Create(params['scheme_name']))

    with NeverUndo(script) as never_undo:
        scheme_name = params['scheme_name']
        permissions = {
            'BROWSE_PROJECTS': {
                'projectRole': ['developers', 'supervisors']},
            'CREATE_ISSUES': {
                'projectRole': ['developers', 'supervisors']},
            'ADMINISTER_PROJECTS': {
                'projectRole': ['developers']}}
        never_undo.do(PermScheme.UpdatePermissions(scheme_name, permissions))
