from python.atlas import Projects
from python.scripts.ExcelScript import ExcelScript
from usr_scripts.excel.widgets import Tables, PieCharts, LineCharts, BarCharts
from usr_scripts.excel.widgets.BarCharts import IssuesResolutionTimes


class IssueStats(ExcelScript):
    """Writes a bunch of graphs and pie charts in the excel file"""

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
            self.put(BarCharts.CreatedCompletedBar(project['key']), ws, col=3)


class SimpleLineChart(ExcelScript):
    """An excel script to try line charts and bar charts"""

    def __init__(self):
        super().__init__('Da title', 'Da description')

    def _generate(self):
        ws = self.new_sheet('Tasks')
        self.put(BarCharts.CommitDiffBar_Atlas('ISLBD', 'private'), ws)
        self.put(BarCharts.CommitDiffBar_Git('ISLBD', 'private'), ws)
        # self.put(LineCharts.BSLine(), ws)
        # self.put(BarCharts.BSBar(), ws, col=2)
        # self.put(IssuesResolutionTimes('ISLBD'), ws)
