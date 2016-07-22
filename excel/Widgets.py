from abc import ABC, abstractmethod
from atlas import Projects
from openpyxl import Workbook
from openpyxl.utils import coordinate_from_string, column_index_from_string, rows_from_range, coordinate_to_tuple


class Widget(ABC):
    def write(self, worksheet, cell='A1'):
        self._fetch()
        self._write(worksheet, cell)

    @abstractmethod
    def _write(self, worksheet, cell):
        pass

    @abstractmethod
    def _fetch(self):
        pass


class Table(Widget):
    def __init__(self):
        self.header = []
        self.rows = []

    def _write(self, worksheet, cell):
        row, col = coordinate_to_tuple(cell)
        rows = list(worksheet.get_squared_range(col, row, col-1+len(self.rows[0]), row-1+len(self.rows)))
        for i, header_cell in enumerate(rows[0]):
            header_cell.value = self.header[i]
        for i, row in enumerate(rows[1:]):
            for j, c in enumerate(row):
                c.value = self.rows[i][j]

    def append(self, *args):
        self.rows.append(args)


class IssuesStatus(Table):
    def __init__(self, project_key):
        super().__init__()
        self.project_key = project_key

    def _fetch(self):
        issues = Projects.GetIssues(self.project_key).do()
        data = {}
        for issue in issues:
            fields = issue['fields']
            name = (fields['assignee'] or {}).get('displayName', 'unassigned')
            resolution = fields['resolution']
            resolution = 'Open' if resolution is None else fields['status']['name']
            if name not in data:
                data[name] = {}
            if resolution not in data[name]:
                data[name][resolution] = 0
            data[name][resolution] += 1

        self.header = ['Assignee', 'Open', 'Resolved', 'Closed']
        for k, v in data.items():
            self.append(k, v.get('Open', 0), v.get('Resolved', 0), v.get('Closed', 0))
