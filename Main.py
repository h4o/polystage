import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from requester.Requester import Requester, CredType
from scripts.atlas import MultiRepo, Students, MultiProjects
from scripts.excel.ExcelScript import IssueStats
from util.util import eprint
from atlas import User, Roles, Applinks, BitbucketPerm, Command, Groups, PermScheme, Projects, Repos, Users

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

Requester.req = Requester(CredType.fab)

def import_students():
    try:
        script = Students.load_all()
    except Exception as e:
        print(e)


def multi_project():
    try:
        script = MultiProjects.load_multi_project('schema/ISL_script.yml')
        # print("\nSuccess, now reverting")
        # script.revert()
    except Exception as e:
        eprint(e)


def devint():
    try:
        script = MultiRepo.load_multi_repo('schema/DEVINT_script.yml')
        # print('\nImport over, reverting')
        # script.revert()
    except Exception as e:
        eprint(e)


def excel_script():
    i = IssueStats('SI3-OGL', 'private')
    # i = IssueStats('ISL', 'private')
    i.generate('Stats.xlsx')


def try_smthing():
    # print(Requester.req)
    Projects.CreateBitbucket('KEYKEY', 'NAMENAME').do()


if __name__ == '__main__':
    # func = lambda: import_students()
    # func = lambda: multi_project()
    # func = lambda: devint()
    # func = lambda: excel()
    # func = lambda: excel_script()
    func = lambda: try_smthing()

    func()
