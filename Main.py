import json
from operator import itemgetter

from openpyxl import Workbook
from texttable import Texttable

from atlas import Projects
from excel import Widgets
from scripts import Scripts

if __name__ == '__main__':
    wb = Workbook()
    ws = wb.active

    status = Widgets.IssuesStatus('ISLBD')
    types = Widgets.IssuesType('ISLBD')

    status.write(ws, 'A1')
    types.write(ws, 'A1', offset_row=status.size[1] + 2)
    types.write(ws, 'A1', offset_col=status.size[0] + 4)

    wb.save('ISLBD.xlsx')



    # Scripts.import_students('students.csv', ['jira-users', 'Les zouzous du dimanche'], create_groups=True)
