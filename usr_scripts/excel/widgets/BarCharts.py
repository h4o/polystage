import collections
from abc import abstractmethod
from datetime import datetime

from python.atlas import Projects, Repos
from python.excel.Widgets import BarChart
from python.util import sort_groupby


class BSBar(BarChart):
    def __init__(self):
        super().__init__('Tasks execution times')
        self.header = ['Task name', 'Worst Execution time (ms)', 'Best Execution Time (ms)']

    def update(self):
        self.append('Mission Task', 0.089, 0.011)
        self.append('Navigate Task', 0.917, 0.162)
        self.append('Refine Task', 29.020, 8.718)
        self.append('Report Task', 53.487, 0.496)
        self.append('Control Task', 0.017, 0.001)
        self.append('Avoid Task', 14.081, 1.165)
        self.append('Communicate Task', 27.049, 11.913)


class CreatedCompletedBar(BarChart):
    def __init__(self, project_key):
        super().__init__('Created / Completed issues')
        self.header = ['User name', 'Issues created', 'Issues completed']
        self.project_key = project_key

    def update(self):
        issues = Projects.GetIssues('ISLBD').do()
        done = [i for i in issues if i['fields']['status']['statusCategory']['name'] == 'Complete' and
                i['fields']['assignee']]

        close_by = sort_groupby(done, lambda i: i['fields']['assignee']['displayName'])
        nb_closed_by = {user: len(list(issues)) for user, issues in close_by}

        created_by = sort_groupby(issues, lambda i: i['fields']['creator']['displayName'])
        nb_created_by = {user: len(list(issues)) for user, issues in created_by}

        for user, nb_created in nb_created_by.items():
            nb_closed = nb_closed_by.get(user, 0)

            self.append(user, nb_created, nb_closed)


class CommitDiffBar(BarChart):
    def __init__(self, project_key, repo):
        super().__init__('Commit differences')
        self.header = ['User', 'Lines added']
        self.project_key = project_key
        self.repo = repo

    @abstractmethod
    def _get_commits(self):
        pass

    def update(self):
        commits = self._get_commits()
        grouped = sort_groupby(commits, key=lambda c: c['author'])

        for author, commits in grouped:
            delta = sum([c['created'] - c['deleted'] for c in commits])
            self.append(author, delta)


class CommitDiffBar_Git(CommitDiffBar):
    def __init__(self, project_key, repo):
        super().__init__(project_key, repo)

    def _get_commits(self):
        return Repos.GetAllCommitsDiffsGit(self.project_key, self.repo).do()


class CommitDiffBar_Atlas(CommitDiffBar):
    def __init__(self, project_key, repo):
        super().__init__(project_key, repo)

    def _get_commits(self):
        return Repos.GetAllCommitDiffs(self.project_key, self.repo).do()


class IssuesResolutionTimes(BarChart):
    def __init__(self, project):
        super().__init__('Issues resolution times')
        self.project = project
        self.header = ['Resolution time(days)', 'Number of issues']

    def update(self):
        issues = Projects.GetIssues('ISLBD').do()
        format_str = '%Y-%m-%dT%H:%M:%S.%f'

        for issue_str in issues:
            creation_date_str = issue_str['fields']['created'].partition('+')[0]
            done_date_str = issue_str['fields']['resolutiondate']

            creation_date = datetime.strptime(creation_date_str, format_str)

            if done_date_str is not None:
                done_date = datetime.strptime(done_date_str.partition('+')[0], format_str)
            else:
                done_date = datetime.now()

            issue_str['fields']['dates'] = {}
            dates = issue_str['fields']['dates']
            dates['created'], dates['resolved'], dates['delta'] = creation_date, done_date, done_date - creation_date

        grouped = sort_groupby(issues, lambda i: i['fields']['dates']['delta'].days)

        for key, issues in grouped:
            self.append(key, len(list(issues)))
