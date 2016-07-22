import json
from operator import itemgetter

from openpyxl import Workbook
from texttable import Texttable

from excel.Widgets import IssuesStatus
from scripts import Scripts

if __name__ == '__main__':
    wb = Workbook()
    ws = wb.active

    s = IssuesStatus('ISLBD')
    s.write(ws, 'E7')
    wb.save('ISLBD.xlsx')



    # Scripts.import_students('students.csv', ['jira-users', 'Les zouzous du dimanche'], create_groups=True)