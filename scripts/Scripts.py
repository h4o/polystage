import csv

from atlas import Users, Permissions, Applinks, Projects, Roles, Repos
from atlas.User import Student
from exceptions import Exceptions
from schema import yaml_loader
from util import eprint


def load_students(user_file):
    users = []
    with open(user_file) as f:
        users_csv = csv.reader(f, delimiter=';')
        for row in users_csv:
            user = Student(row)
            users.append(user)
    return users


def remove_students(user_file):
    students = load_students(user_file)
    Users.RemoveMany(students).do()


def import_students(user_file, groups, create_groups=False):
    students = load_students(user_file)
    s = Script()
    for student in students:
        s.append(Users.Create(student))
    s.append(Users.AddManyToGroups(students, groups, create_groups))
    s.execute()


class Script:
    def __init__(self):
        self.commands = []

    def append(self, command):
        self.commands.append(command)

    def execute(self):
        p = 0
        try:
            for i, cmd in enumerate(self.commands):
                p = i
                cmd.do()
        except Exceptions.RequestException as e:
            eprint('Failure: ', e, '\nTrying to undo:')
            self._revert(p)

    def _revert(self, i):
        undo_list = self.commands[0:i][::-1]
        for cmd in undo_list:
            cmd.undo()

#
#

#
#

#
# def import_projects(file_path):
#     p = yaml_loader.load(file_path, 'schema/project_schema.yml')
#     params = p['global']
#     projects = p['projects']
#
#     Permissions.create(params['tag'])
#
#     for project in projects:
#         _import_project(project, params)
#
#     Permissions.create_permission(params['tag'], 'projectRole', 'developers', 'BROWSE_PROJECTS')
#     Permissions.create_permission(params['tag'], 'projectRole', 'supervisors', 'BROWSE_PROJECTS')
#     Permissions.create_permission(params['tag'], 'projectRole', 'supervisors', 'ADMINISTER_PROJECTS')
#
#
# def _import_project(project, params):
#     project_type = params.get('type', 'business')
#     key = project.get('key') or _name_to_key(project['name'])
#
#     Projects.create_jira(key, project['name'], project['lead'], project_type=project_type)
#     Projects.create_bitbucket(key, project['name'])
#
#     dev_role = Roles.get('developers') or Roles.create('developers', 'The developers of the project')
#     sup_role = Roles.get('supervisors') or Roles.create('supervisors', 'The supervisors of the project')
#
#     if params.get('applink', True):
#         Applinks.link(key, key)
#
#     Projects.add_with_role(key, params['admin'], 'supervisors')
#     for dev in project['developers']:
#         Projects.add_with_role(key, dev, dev_role['name'])
#     for sup in project.get('supervisors', []):
#         Projects.add_with_role(key, sup, sup_role['name'])
#
#     repos = params.get('repositories', None)
#     if repos is not None:
#         for repo in repos:
#             Repos.create(key, repo)
#
#     Permissions.assign_to_project(key, params['tag'])
#
#
# def import_multi_repo(multi_repo_file):
#     projects = yaml_loader.load(multi_repo_file, 'schema/multi_repo_schema.yml')
#     params, repos = projects['global'], projects['repositories']
#     params['key'] = params.get('key') or _name_to_key(params['name'])
#     params['applink'] = params.get('applink', False)
#     params['type'] = params.get('type', 'business')
#
#     Projects.create_jira(params['key'], params['name'], params['admin'], project_type=params['type'])
#     Projects.create_bitbucket(params['key'], params['name'])
#
#     Roles.get('developers') or Roles.create('developers', '')
#     Roles.get('supervisors') or Roles.create('supervisors', '')
#
#     Projects.add_with_role(params['key'], params['admin'], 'supervisors')
#     for supervisor in params['supervisors']:
#         Projects.add_with_role(params['key'], supervisor, 'supervisors')
#     developers = set.union(*[set(r['developers']) for r in repos])
#     for dev in developers:
#         Projects.add_with_role(params['key'], dev, 'developers')
#
#     Permissions.create(params['name'])
#     Permissions.assign_to_project(params['key'], params['name'])
#     Permissions.create_permission(params['name'], 'projectRole', 'developers', 'BROWSE_PROJECTS')
#     Permissions.create_permission(params['name'], 'projectRole', 'supervisors', 'ADMINISTER_PROJECTS')
#     Permissions.create_permission(params['name'], 'projectRole', 'supervisors', 'BROWSE_PROJECTS')
#
#     if params['applink']:
#         Applinks.link(params['key'], params['key'])
#
#     for repo in repos:
#         _create_set_repo(repo, params)
#
#
# def _create_set_repo(repo, params):
#     Repos.create(params['key'], repo['name'])
#     # TODO set permissions
#
#
# def _name_to_key(name):
#     return name[:10].replace(' ', '').upper()
