import csv

from atlas import Users, Permissions, Applinks, Projects, Roles, Repos
from atlas.User import Student
from schema import yaml_loader


def load_students(user_file):
    users = []
    with open(user_file) as f:
        users_csv = csv.reader(f, delimiter=';')
        for row in users_csv:
            user = Student(row)
            users.append(user)
    return users


def import_students(user_file, groups, create_groups=False):
    students = load_students(user_file)
    Users.create_many(students)
    Users.add_many_to_groups(students, groups, create_groups)


def remove_students(user_file):
    students = load_students(user_file)
    Users.remove_many(students)


def import_projects(file_path):
    p = yaml_loader.load(file_path, 'schema/project_schema.yml')
    params = p['global']
    projects = p['projects']

    Permissions.create(params['tag'])

    for project in projects:
        _import_project(project, params)

    Permissions.create_permission(params['tag'], 'projectRole', 'developers', 'BROWSE_PROJECTS')
    Permissions.create_permission(params['tag'], 'projectRole', 'supervisors', 'ADMINISTER_PROJECTS')


def _import_project(project, params):
    project_type = params.get('type', 'business')
    key = project.get('key') or project['name'][:10].replace(' ', '').upper()

    Projects.create_jira(key, project['name'], project['lead'], project_type=project_type)
    Projects.create_bitbucket(key, project['name'])

    dev_role = Roles.get('developers') or Roles.create('developers', 'The developers of the project')
    sup_role = Roles.get('supervisors') or Roles.create('supervisors', 'The supervisors of the project')

    Applinks.link(key, key)

    for dev in project['developers']:
        Projects.add_with_role(key, dev, dev_role['id'])
    for sup in project.get('supervisors', []):
        Projects.add_with_role(key, sup, sup_role['id'])

    repos = params.get('repositories', None)
    if repos is not None:
        for repo in repos:
            Repos.create(key, repo)

    Permissions.assign_to_project(key, params['tag'])
