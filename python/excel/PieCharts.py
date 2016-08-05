import itertools

from python.atlas import Projects, Repos

from python.excel.Widgets import PieChart


class AssigneePieChart(PieChart):
    def __init__(self, project_key):
        super().__init__('Issues assignees')
        self.project_key = project_key

    def update(self):
        issues = Projects.GetIssues(self.project_key).do()
        assigned = [i for i in issues if i['fields']['assignee'] is not None]
        unassigned = [i for i in issues if i['fields']['assignee'] is None]
        assigned = sorted(assigned, key=lambda x: x['fields']['assignee']['displayName'])
        for k, g in itertools.groupby(assigned, lambda x: x['fields']['assignee']['displayName']):
            self.append(k, len(list(g)))
        self.append('unassigned', len(unassigned))


class IssuesStatusPieChart(PieChart):
    def __init__(self, project_key):
        super().__init__('Issues Status')
        self.project_key = project_key

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

        for k, v in data.items():
            self.append(k, v)


class CommitsPie(PieChart):
    def __init__(self, project_key, repo_name):
        super().__init__('Commits')
        self.repo_name = repo_name
        self.project_key = project_key

    def update(self):
        commits = Repos.GetCommits(self.project_key, self.repo_name).do()
        c = sorted(commits, key=lambda x: x['author']['name'])
        c = itertools.groupby(c, lambda x: x['author']['name'])
        for name, commits in c:
            self.append(name, len(list(commits)))
