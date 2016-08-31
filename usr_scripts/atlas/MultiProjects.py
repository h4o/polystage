from math import floor, log

from python.atlas import Projects, PermScheme, Applinks, Repos, Boards
from python.atlas.Boards import BoardType
from python.schema.yaml_loader import load_file
from python.scripts.Script import ReversibleRunner, NeverUndo, command
from python.scripts.Util import create_basic_roles, grant_bitbucket_perms, add_users_to_project
from python.util import to_ascii


@command
def load(file_name):
    """Load the projects described in the yaml file given in parameters"""
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
    params['board'] = params.get('board', BoardType.KANBAN)
    _set_projects_ids(file)
    for project in file['projects']:
        project['key'] = params['tag'] + project['id']
        project['name'] = project.get('name', project['key'])
        project['lead'] = project.get('lead', project['developers'][0])
        project['supervisors'] = set(params['supervisors'] + project.get('supervisors', []))
        project['readers'] = set(params['readers'] + project.get('readers', []))
    return file


def _set_projects_ids(file):
    base = 26
    no_id = [project for project in file['projects'] if 'id' not in project]
    if not no_id:
        return
    nb_digit = floor(log(len(no_id), base)) + 1
    for ctr, project in enumerate(no_id):
        project['id'] = to_ascii(ctr, nb_digit, base)


def _create_project(project, params, script):
    key, name, lead = project['key'], project['name'], project['lead']
    p_type, tag = params['type'], params['tag']
    readers, supervisors, developers = project['readers'], project['supervisors'], project['developers']

    script.do(Projects.CreateJira(key, name, lead, project_type=p_type, category=tag))
    script.do(Projects.CreateBitbucket(key, name))

    script.do(Boards.Create(params['board'], name))

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
