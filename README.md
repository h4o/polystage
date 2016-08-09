#Atlas Command Line Interface

##Prerequisites
To run this project all you need is a functional installation of Docker

##How to 
Start by cloning this repository:
`git clone https://github.com/h4o/polystage.git`

Then go into the cloned repository and run the build script:
`./build.sh`

You'll never have to do this again.

Now you have to supply some information. Open the file `credentials.yml` in the folder `data` and complete the fields.

You can now run the Atlas CLI:
`./run.sh`

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
Or select only the parts you need
`from python.atlas import Projects, Users`

It's highly advised that you don't run the commands yourself. Instead, make use of the `ReversibleRunner`

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
 

##Adding excel scripts
You can also add your own excel scripts. All you have to you is to implement the class `python.scripts.ExcelScript.ExcelScript`:

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
            
You can run such script by `IssueStats.generate('File_name.xlsx')`
You should never have to run `generate` yourself.

