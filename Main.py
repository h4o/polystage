
from exceptions import Exceptions
from scripts import Scripts
from atlas import Permissions, Projects, Repos, Applinks, Groups, Roles, User, Users
from util import eprint

if __name__ == '__main__':
    # Scripts.import_projects('schema/project_sample.yml')
    # Scripts.import_multi_repo('schema/multi_repo_sample.yml')

    # Projects.CreateBitbucket('ANNOT', 'To delete').do(safe=False)
    # Projects.CreateBitbucket('ANNOT', 'To delete').do(safe=True)
    # Projects.CreateBitbucket('ANNOT', 'To delete').do(safe=True)
    # Projects.delete_bitbucket('ANNOT', safe=True)
    # Projects.DeleteBitbucket('ANNOT').do()

    # cmd.do(safe=True)
    # cmd.undo()

    # noKwargs('First param')
    # noKwargs('First param, safe', safe=True)
    # yesKwargs('First param')
    # yesKwargs('First param, safe', safe=True)
    # yesKwargs('First param', kone='kone', yaya='youyou')
    # yesKwargs('First param, safe', kone='kone', safe=True)
    #
    #
    # name = "OKKOOKKO"
    # Projects.DeleteBitbucket(name).do(safe=True)
    # print('______________________________')
    #
    # create = Projects.CreateBitbucket(name, name)
    # delete = Projects.DeleteBitbucket(name)
    # s = Script()
    # s.append(create)
    # s.append(create)
    # s.append(delete)
    #
    # s.execute()

    # Scripts.remove_students('students.csv')
    Scripts.import_students('students.csv', ['jira-users', 'Les zouzous du dimanche'], create_groups=True)










    # from atlas import Projects, Permissions
    # Projects.delete_jira('PROJECTDE')
    # Projects.delete_bitbucket('PROJECTDE')
    # Permissions.delete('Demo')
