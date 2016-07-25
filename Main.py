from openpyxl import Workbook
from excel import Widgets
from scripts import Scripts, projects
from schema.yaml_loader import load
from util.util import pp

if __name__ == '__main__':
    i = 3

    if i == 0:
        Scripts.import_students('students.csv', ['jira-users', 'Les zouzous du dimanche'], create_groups=True)
    if i == 1:
        wb = Workbook()
        ws = wb.active

        status = Widgets.IssuesStatus('ISLBD')
        types = Widgets.IssuesType('ISLBD')

        status.write(ws, 'A1')
        types.write(ws, 'A1', offset_row=status.size[1] + 2)
        types.write(ws, 'A1', offset_col=status.size[0] + 4)

        wb.save('ISLBD.xlsx')
    if i == 2:
        pass
    if i == 3:
        file = projects.create_multi_project('schema/ISL_script.yml')
