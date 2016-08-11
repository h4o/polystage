#Atlas Command Line Interface

##Prerequisites
To run this project all you need is a functional installation of Docker.

##How to 
Start by cloning this repository:

    git clone https://github.com/h4o/polystage.git

Then go into the cloned repository and run the build script:
    
    ./build.sh

You should never have to do this again.

You have to supply some credentials for the cli to run with the correct rights. Open the file `credentials.yml` in the folder `data` and fill the blanks.

You can now run the Atlas CLI:
    
    ./run.sh

##In details
You can find the three folders `data`, `usr_scripts` and`python`
`python` is the code of the project, you should never have to look into it.
`data` contains any file you need to configure your scripts. When a script need a file, it looks for it in the folder `data` first.
`usr_scripts`contains the scripts you can run. Any python module in this folder is automatically loaded whe the application starts.


##Adding new scripts
To add new scripts, you just need to put them in the folder `usr_scripts` and run the CLI. The autocompletion will guide you.

Scripts are written in python.
You can import every commands this way:
`from python.atlas import *`
Or select only the parts you need:
`from python.atlas import Projects, Users`

It's highly advised that you don't run the commands yourself. Instead, make use of the `ReversibleRunner`.

###Example:

    from python.atlas import Projects, Users, Repos, BitbucketPerm
    from python.atlas.BitbucketPerm import Permission
    from python.scripts.Script import ReversibleRunner, NeverUndo, public

    @public
    def do_the_thing():
        script = ReversibleRunner()
        script.do(Projects.CreateBitbucket('EXAMPLE', 'An example'))
        script.do(Repos.Create('EXAMPLE', 'Repo-One'), never_undo=True)
    
        with NeverUndo(script) as never_undo:
            never_undo.do(BitbucketPerm.GrantPermission('EXAMPLE', 'crowd', Permission.ADMIN))
  
When a script uses the `ReversibleRunner`, any command failure will trigger a revert process to undo the previous commands.

If some commands are run with the parameter `never_undo=True` or with
    
    with NeverUndo(script) as never_undo:
        never_undo.do(...)
then, any failure will still trigger a revert process, but will never try to undo these commands. 

In this example, if your module's name is `ThingDoer.py` you can run it directly with the following command. 
    
    ThingDoer.do_the_thing() 

##Adding excel scripts
You can also add your own excel scripts. To do so, simply derive from the class `python.scripts.ExcelScript.ExcelScript` and implement the method `_generate`
You have to methods at your disposal to handle the excel file.

`self.new_sheet()` which will create and return a new worksheet of the name given in parameters.
`self.put()` which write the given widget in the given worksheet. Put's `col` parameter can be set to arrange the widgets horizontally.

You can also use any command from `python.atlas` to retrieve needed information.

###Example

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
            
If this class is defined in the module `Sample` you can run it typing:

    Sample.IssueStats('SI3-OGL', 'private').generate('File_name.xlsx')
You should never have to run `_generate` directly.


##The widgets
There are currently two kinds of widgets : `Table` and `PieChart` from `python.excel.Widgets`, and both can be extended by implementing the method `update` which purpose is to retrieve the data used to write the Table or draw the Pie Chart.
In excel, everything is more or less a table. So both the Table and the PieChart need to be given its data in a table form, through the class member `self.rows`, which is a list of the table rows (a list of list of strings), and `self.header`, which is the header of the table.
You can use the method `self.append` to add values to the bottom of your table.

The creation of the PieChart only take into account the two first columns of its table. The left one for the labels and the right one for the values. 

###Example

    class SamplePieChart(PieChart):
        def __init__(self):
            super().__init__('Pet Ownership')
    
        def update(self):
            self.header = ['Pet', 'Ownership']
            self.rows =  [['Dogs',         55],
                          ['Cats',         30],
                          ['Fish',          6],
                          ['Rabbits',       5],
                          ['Rodents',       4]]