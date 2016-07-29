import json
import time
from openpyxl import Workbook

from atlas import Projects, Users, PermScheme, Repos, Groups
from atlas.BitbucketPerm import Permission
from atlas.ExcelScript import IssueStats
from excel import Widgets
from requester import Requester
from requester.Requester import CredType, req
from scripts import Runner, MultiProjects, Students, MultiRepo
from schema.yaml_loader import load
from scripts.Runner import ReversibleRunner
from util.util import pp, eprint

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def import_students():
    try:
        script = Students.import_students('students.csv', ['jira-users', 'Les poids lourds de l\'amour'])
    except Exception as e:
        print(e)


def multi_project():
    try:
        script = MultiProjects.load_multi_project('schema/ISL_script.yml')
        print("\nSuccess, now reverting")
        time.sleep(10)
        script.revert()
    except Exception as e:
        eprint(e)


def multi_repos():
    try:
        script = MultiRepo.load_multi_repo('schema/DEVINT_script.yml')
        print('\nImport over, reverting')
        script.revert()
    except Exception as e:
        eprint(e)


def excel():
    wb = Workbook()
    ws = wb.active

    status = Widgets.IssuesStatus('ISLBD')
    types = Widgets.IssuesType('ISLBD')
    pie = Widgets.PieChart('ISLBD')

    status.write(ws, 'A1')
    types.write(ws, 'A1', offset_row=status.size[1] + 2)

    pie.write(ws, 'A16')

    wb.save('ISLBD.xlsx')


def excel_script():
    i = IssueStats('ISL')
    i.generate('Stats.xlsx')


def try_smthing():
    # p = Projects.GetJira('PFE').do()
    # p = Projects.GetJira('PFEAL').do()
    # c = Projects.CreateCategory('Blabadoo').do()
    # pp(c)
    # pp(p)
    # print(json.dumps(p))
    # p = Projects.GetCategory('POG').do()

    # Projects.CreateCategory('TEST').do()
    # Projects.CreateJira('TESTAA', 'TESTAA', 'crowd', category='TEST').do(safe=True)
    Projects.DeleteJira('TESTAA').do(safe=True)
    # Projects.DeleteCategory('TEST').do()


if __name__ == '__main__':
    # func = lambda: import_students()
    func = lambda: multi_project()
    # func = lambda: multi_repos()
    # func = lambda: excel()
    # func = lambda: excel_script()
    # func = lambda: try_smthing()

    func()