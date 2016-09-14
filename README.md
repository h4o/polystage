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
Scripts are high level python modules using commands. They are meant to be run though the CLI.
To add new scripts, you just need to put them in the folder `usr_scripts/atlas` and run the CLI. The autocompletion will guide you.

You can import in your script every commands this way:
`from python.atlas import *`
Or select only the modules you need:
`from python.atlas import Projects, Users`

###In short
- Scripts are python modules (files) in which a function is annotated `@command` and this function returns a `ReversibleRunner`
- Scripts are placed in the folder `usr_scripts/atlas`
- Scripts are run by the CLI with the name of the module
- The CLI runs the method annotated `@command`

###Example:

    # MyScript.py
    from python.atlas import Projects, Users, Repos, BitbucketPerm
    from python.atlas.BitbucketPerm import Permission
    from python.scripts.Script import ReversibleRunner, NeverUndo, public

    @command
    def do_the_thing(param1, param2):
        """Does the thing it's supposed to do. This comment with be displayed when the Help command is invoked"""
        script = ReversibleRunner()
        script.do(Projects.CreateBitbucket('EXAMPLE', 'An example'))
        script.do(Repos.Create('EXAMPLE', 'Repo-One'), never_undo=True)
    
        with NeverUndo(script) as never_undo:
            never_undo.do(BitbucketPerm.GrantPermission('EXAMPLE', 'crowd', Permission.ADMIN))
        
        return ReversibleRunner()
  
Here, the module's name is MyScript. To run this script, the user will use the command `MyScript`.
The function `do_the_thing` is annotated `@command` which makes it the entry point of the script. Its parameters are the parameters of the script. The user will have to include them in the command: `MyScript param1_value param2_value`
Since a script uses the `ReversibleRunner`, any command failure will trigger a revert process to undo the previous commands.
The instance of the `ReversibleRunner` used to run the commands is returned at the end, so the user can manually undo the script with the command `undo`

###The never_undo methods
If some commands are run with the parameter `never_undo=True` or with

    with NeverUndo(script) as never_undo:
        never_undo.do(...)
then, any failure will still trigger a revert process, but will never try to undo these commands.

###Example:

    # Students.py
    
    @command
    def load(user_file='data/students'):
        """Import every users from the csv file"""
        script = ReversibleRunner()
         
         ...
    
        for student in students:
            script.do(Users.Create(student))
            for group in groups:
                script.do(Users.AddToGroup(student.username, group), never_undo=True)
    
        return script
        
This is a portion of a real script creating users and adding them to groups. Every students will be added to every groups.
Because of the `ReversibleRunner` if the command `AddToGroup` fails, every previous commands will be undone.
Now imagine if the addition in the last group of the last student in the list fails. The script will have to remove every student from the groups to which he belongs then deleting the student when he could have done the deletion only.
The `never_undo` parameter you can see set to `True` will tell the script it doesn't need to undo this action after a failure. So the only undoable operation remaining are the users creations. 


##Adding excel scripts
Excel scripts are high level python classes using widgets (Charts, tables, ...) to generate a Excel file.

To implement you own excel scripts simply derive from the class `python.scripts.ExcelScript.ExcelScript` and implement the method `_generate`
You have two methods at your disposal to handle the excel file.

`self.new_sheet()` which will create and return a new worksheet of the name given in parameters.
`self.put()` which write the given widget in the given worksheet. Put's `col` parameter can be set to arrange the widgets horizontally.

###In short
- An excel script inherits the class `ExcelScript` and implement the method `_generate`
- Excel scripts are placed in the folder `usr_scripts/excel`
- Excel scripts are run by the CLI with its direct name (the name of the class). Its parameters are the same as its constructor's
- The CLI will always add a parameter to the command which is the name of the file to be generated
- Excel scripts manipulates widgets and excel worksheets with the methods `self.new_sheet()` and `self.put(widget, sheet)`
- Calling its super constructor with the arguments `title` and `description` will add put a header in the worksheets with the date the file was generated

###Example

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
            
This class implements `ExcelScript` and its method `_generate`.
Its constructor has two parameters `project_tag` and `repos_name`. The CLI command to execute this script is: `IssueStats project_tag_value repos_name_value file_name`. Don't forget that the name of the generated file will always be the last parameter of an excel script.

The class is commented, so the CLI command `help IssueStats` will display `Writes a bunch of graphs and pie charts in the excel file` when called.

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