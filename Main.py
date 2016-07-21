import json
from operator import itemgetter

from openpyxl import Workbook
from texttable import Texttable

from excel.Widgets import IssuesStatus
from exceptions import Exceptions
from requester.Requester import req
from scripts import Scripts
from atlas import Permissions, Projects, Repos, Applinks, Groups, Roles, User, Users
from util import eprint

if __name__ == '__main__':
    wb = Workbook()
    ws = wb.active

    s = IssuesStatus('ISLBD')
    s.write(ws, 0, 0)
    wb.save('ISLBD.xlsx')
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
    # Scripts.import_students('students.csv', ['jira-users', 'Les zouzous du dimanche'], create_groups=True)
