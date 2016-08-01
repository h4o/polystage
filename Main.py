import json
import time
from itertools import groupby

from openpyxl import Workbook

import excel.Tables
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
        # script.revert()
    except Exception as e:
        eprint(e)


def multi_repos():
    try:
        script = MultiRepo.load_multi_repo('schema/DEVINT_script.yml')
        print('\nImport over, reverting')
        # script.revert()
    except Exception as e:
        eprint(e)


def excel_script():
    i = IssueStats('SI3-OGL')
    # i = IssueStats('ISL')
    i.generate('Stats.xlsx')


def try_smthing():
    pass


if __name__ == '__main__':
    # func = lambda: import_students()
    # func = lambda: multi_project()
    # func = lambda: multi_repos()
    # func = lambda: excel()
    func = lambda: excel_script()
    # func = lambda: try_smthing()

    func()
