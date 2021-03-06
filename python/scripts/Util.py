from python.atlas import BitbucketPerm
from python.atlas import Roles, Projects
from python.atlas.BitbucketPerm import Permission


def create_basic_roles(script):
    """Create the default roles developers, supervisors and readers if they don't already exists"""
    roles = script.do(Roles.GetAll())
    roles = [a['name'] for a in roles]

    'developers' in roles or script.do(Roles.Create('developers'))
    'supervisors' in roles or script.do(Roles.Create('supervisors'))
    'readers' in roles or script.do(Roles.Create('readers'))


def grant_bitbucket_perms(project_key, script, readers=None, writers=None, admins=None):
    readers = readers or []
    writers = writers or []
    admins = admins or []
    for reader in readers:
        script.do(BitbucketPerm.GrantPermission(project_key, reader, Permission.READ))
    for developer in writers:
        script.do(BitbucketPerm.GrantPermission(project_key, developer, Permission.WRITE))
    for supervisor in admins:
        script.do(BitbucketPerm.GrantPermission(project_key, supervisor, Permission.ADMIN))


def grant_bitbucket_repo_perms(project_key, repo_name, script, readers=None, writers=None, admins=None):
    readers = readers or []
    writers = writers or []
    admins = admins or []
    for reader in readers:
        script.do(BitbucketPerm.GrantRepoPermission(project_key, repo_name, reader, Permission.R_READ))
    for developer in writers:
        script.do(BitbucketPerm.GrantRepoPermission(project_key, repo_name, developer, Permission.R_WRITE))
    for supervisor in admins:
        script.do(BitbucketPerm.GrantRepoPermission(project_key, repo_name, supervisor, Permission.R_ADMIN))


def add_users_to_project(project_key, script, readers=None, developers=None, supervisors=None):
    readers = readers or []
    developers = developers or []
    supervisors = supervisors or []
    for reader in readers:
        script.do(Projects.AddWithRole(project_key, reader, 'readers'))
    for developer in developers:
        script.do(Projects.AddWithRole(project_key, developer, 'developers'))
    for supervisor in supervisors:
        script.do(Projects.AddWithRole(project_key, supervisor, 'supervisors'))
