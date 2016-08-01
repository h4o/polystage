from atlas import Projects
from excel.Widgets import Table


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