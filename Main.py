import time
from openpyxl import Workbook

from atlas import Projects, Users, Permissions, Repos, Groups
from excel import Widgets
from scripts import Scripts, MultiProjects, Students, MultiRepo
from schema.yaml_loader import load
from scripts.Scripts import ReversibleRunner
from util.util import pp, eprint

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if __name__ == '__main__':
    i = 4

    if i == 0:
        try:
            script = Students.import_students('students.csv', ['jira-users', 'Les poids lourds de l\'amour'])
            # script.revert()
            # Scripts.remove_students('students.csv')
        except Exception as e:
            eprint(e)
    if i == 1:
        wb = Workbook()
        ws = wb.active

        status = Widgets.IssuesStatus('ISLBD')
        types = Widgets.IssuesType('ISLBD')
        pie = Widgets.Pie('ISLBD')

        status.write(ws, 'A1')
        types.write(ws, 'A1', offset_row=status.size[1] + 2)

        pie.write(ws, 'A16')

        wb.save('ISLBD.xlsx')
    if i == 2:
        Projects.DeleteJira('ISLAA').do(safe=True)
        Projects.DeleteJira('ISLAB').do(safe=True)
        Projects.DeleteJira('Cobblestone').do(safe=True)
    if i == 3:
        try:
            MultiProjects.load_multi_project('schema/ISL_script.yml')
            print("\nSuccess, now reverting")
            # script.revert()
        except Exception as e:
            eprint(e)
            # raise(e)
    if i == 4:
        script = None
        try:
            script = MultiRepo.load_multi_repo('schema/DEVINT_script.yml')
            print('\nImport over, reverting')
            script.revert()
        except Exception as e:
            eprint(e)
            # raise e
