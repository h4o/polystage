from abc import ABC, abstractmethod

from openpyxl.chart import Reference, PieChart
from openpyxl.chart.marker import DataPoint

from atlas import Projects
from openpyxl import Workbook
from openpyxl.utils import coordinate_from_string, column_index_from_string, rows_from_range, coordinate_to_tuple, \
    get_column_letter

from util.util import pp


class Widget(ABC):
    def write(self, worksheet, cell='A1', offset_col=0, offset_row=0):
        row, col = coordinate_to_tuple(cell)
        cell = get_column_letter(col + offset_col) + str(row + offset_row)

        self._write(worksheet, cell)

    @abstractmethod
    def _write(self, worksheet, cell):
        pass

    @abstractmethod
    def update(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass


class Table(Widget):
    def __init__(self):
        self.header = []
        self.rows = []

    def _write(self, worksheet, cell):
        row, col = coordinate_to_tuple(cell)
        size_x, size_y = self.size
        rows = list(worksheet.get_squared_range(col, row, col + size_x - 1, row + size_y - 1))
        for i, header_cell in enumerate(rows[0]):
            header_cell.value = self.header[i]
        for i, row in enumerate(rows[1:]):
            for j, c in enumerate(row):
                c.value = self.rows[i][j]

    def append(self, *args):
        self.rows.append(args)

    @property
    def size(self):
        y = len(self.rows)
        x = 0 if y == 0 else len(self.rows[0])
        return x, y + 1


class Pie(Table):
    def __init__(self, project_key):
        super().__init__()
        self.project_key = project_key

    def _write(self, worksheet, cell):
        super(Pie, self)._write(worksheet, cell)

        row, col = coordinate_to_tuple(cell)

        pie = PieChart()
        labels = Reference(worksheet, min_col=col, min_row=row + 1, max_row=row + len(self.rows))
        data = Reference(worksheet, min_col=col + 1, min_row=row, max_row=row + len(self.rows))
        pie.add_data(data, titles_from_data=True)
        pie.set_categories(labels)
        pie.title = "Issues"
        worksheet.add_chart(pie, cell)

    def update(self):
        issues = Projects.GetIssues(self.project_key).do()
        data = {}
        for issue in issues:
            fields = issue['fields']
            resolution = fields['resolution']
            resolution = 'Open' if resolution is None else fields['status']['name']

            if resolution not in data:
                data[resolution] = 0
            data[resolution] += 1

        self.header = ['Key', 'Values']
        for k, v in data.items():
            self.append(k, v)


class IssuesStatus(Table):
    def __init__(self, project_key):
        super().__init__()
        self.project_key = project_key

    def update(self):
        issues = Projects.GetIssues(self.project_key).do()
        data = {}
        for issue in issues:
            fields = issue['fields']
            assignee = (fields['assignee'] or {}).get('displayName', 'unassigned')
            resolution = fields['resolution']
            resolution = 'Open' if resolution is None else fields['status']['name']
            if assignee not in data:
                data[assignee] = {'Assignee': assignee}
            if resolution not in data[assignee]:
                data[assignee][resolution] = 0
            data[assignee][resolution] += 1

        self.header = ['Assignee', 'Open', 'Resolved', 'Closed']
        tuples = sorted(data.values(), key=lambda i: i['Assignee'])
        self.rows = []
        for t in tuples:
            self.append(t.get('Assignee'), t.get('Open', 0), t.get('Resolved', 0), t.get('Closed', 0))


class IssuesType(Table):
    def __init__(self, project_key, types=None):
        self.types = types or ['Bug', 'Improvement', 'New Feature', 'Sub-task', 'Task', 'Technical task']
        super().__init__()
        self.project_key = project_key

    def update(self):
        issues = Projects.GetIssues(self.project_key).do()
        result = [a for a in Projects.GetIssueTypes().do() if a['name'] in self.types]
        issue_types = {}
        for i in result:
            issue_types[i['id']] = i
        data = {}
        for issue in issues:
            fields = issue['fields']
            assignee = (fields['assignee'] or {}).get('displayName', 'unassigned')
            type_id = fields['issuetype']['id']
            if type_id in issue_types:
                name = issue_types[type_id]['name']
                if assignee not in data:
                    data[assignee] = {'Assignee': assignee}
                if name not in data[assignee]:
                    data[assignee][name] = 0
                data[assignee][name] += 1

        self.header = ['Assignee'] + self.types
        tuples = sorted(data.values(), key=lambda i: i['Assignee'])
        self.rows = []
        for t in tuples:
            values = [t['Assignee']]
            for type_field in self.types:
                values.append(t.get(type_field, 0))
            self.append(*values)
