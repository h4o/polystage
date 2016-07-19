from scripts import Scripts
from atlas import Permissions, Projects, Repos, Applinks, Groups, Roles, User, Users

if __name__ == '__main__':
    # Scripts.import_projects('schema/project_sample.yml')
    # Scripts.import_multi_repo('schema/multi_repo_sample.yml')

    Repos.delete('DEVINT', 'qdskjlkzkzkk')














    # from atlas import Projects, Permissions
    # Projects.delete_jira('PROJECTDE')
    # Projects.delete_bitbucket('PROJECTDE')
    # Permissions.delete('Demo')