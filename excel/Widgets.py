from abc import ABC, abstractmethod

from atlas import Projects


class Widget(ABC):
    def write(self, worksheet, col, line):
        self._fetch()
        self._write(worksheet, col, line)

    @abstractmethod
    def _write(self, worksheet, col, line):
        pass

    @abstractmethod
    def _fetch(self):
        pass


class Table(Widget):
    def __init__(self):
        self.header = []
        self.rows = []

    def _write(self, worksheet, col, line):
        worksheet.append(self.header)
        for row in self.rows:
            worksheet.append(row)

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
