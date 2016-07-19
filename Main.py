from exceptions import Exceptions
from scripts import Scripts
from atlas import Permissions, Projects, Repos, Applinks, Groups, Roles, User, Users
from util import eprint

if __name__ == '__main__':
    # Scripts.import_projects('schema/project_sample.yml')
    # Scripts.import_multi_repo('schema/multi_repo_sample.yml')

    Projects.create_bitbucket('ANNOT', 'To delete', safe=True)
    Projects.create_bitbucket('ANNOT', 'To delete', safe=True)
    # Projects.delete_bitbucket('ANNOT', safe=True)
    Projects.delete_bitbucket('ANNOT')

    # noKwargs('First param')
    # noKwargs('First param, safe', safe=True)
    # yesKwargs('First param')
    # yesKwargs('First param, safe', safe=True)
    # yesKwargs('First param', kone='kone', yaya='youyou')
    # yesKwargs('First param, safe', kone='kone', safe=True)












    # from atlas import Projects, Permissions
    # Projects.delete_jira('PROJECTDE')
    # Projects.delete_bitbucket('PROJECTDE')
    # Permissions.delete('Demo')
