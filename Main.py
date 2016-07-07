import Groups
import Users

Groups.delete(['4a-2015'])
Users.remove_students('students.csv')
Users.import_students('students.csv', ['jira-users', '4a-2015'], create_groups=True)
