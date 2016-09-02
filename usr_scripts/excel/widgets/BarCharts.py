from python.atlas import Projects
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
