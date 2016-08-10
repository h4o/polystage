from python.atlas import Projects
from python.excel import Tables, PieCharts
from python.scripts.ExcelScript import ExcelScript


class IssueStats(ExcelScript):
    def __init__(self, project_tag, repos_name):
        super().__init__()
        self.repos_name = repos_name
        self.tag = project_tag

    def _generate(self):
        projects = Projects.GetFromTag(self.tag).do()
        for project in projects:
            ws = self.new_sheet(project['key'])
            self.put(Tables.IssuesStatus(project['key']), ws)
            self.put(Tables.IssuesType(project['key']), ws)
            self.put(PieCharts.IssuesStatusPieChart(project['key']), ws, col=2)
            self.put(PieCharts.AssigneePieChart(project['key']), ws, col=2)
            self.put(PieCharts.CommitsPie(project['key'], self.repos_name), ws)